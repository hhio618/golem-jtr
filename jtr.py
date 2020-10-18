#!/usr/bin/env python3
import asyncio
import pathlib
import sys
import argparse

import yapapi
from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta


async def main(num_nodes, password, timeout, subnet_tag="devnet-alpha.2" ):
    package = await vm.repo(
        image_hash="2026963e90ff855defe7dbd503660a1d7ff4bfc7dd76eff03b8383ca",
        min_mem_gib=0.5,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            node_no = task.data
            result = "result_node_{}.txt".format(node_no)
            cmd = f"/golem/entrypoints/entrypoint.sh {password} {timeout} {node_no} {num_nodes}"
            print(f"\033[36;1mRunning {cmd} on node#{node_no}\033[0m")
            ctx.run("sh", "-c", f"{cmd} >> /golem/output/log.txt 2>&1")
            ctx.download_file("/golem/output/result.txt", result)
            yield ctx.commit()
            task.accept_task(result=result)

        ctx.log("no more task to run")

    init_overhead: timedelta = timedelta(minutes=10)

    # By passing `event_emitter=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Engine(
        package=package,
        max_workers=num_nodes,
        budget=100.0,
        timeout=init_overhead + timedelta(minutes=num_nodes * 2),
        subnet_tag=subnet_tag,
        event_emitter=log_summary(),
    ) as engine:

        async for task in engine.map(worker, [Task(data=str(node_index+1)) for node_index in range(num_nodes)]):
            print(f"\033[36;1mTask computed: {task}, result: {task.output}\033[0m")
        
    for i in range(num_nodes):
            with open("result_node_{}.txt".format(i+1)) as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("?"):
                        password = line.split(":")[1]
                        print(f"\033[36;1mPassword found: {password}, Node: node_{i+1}\033[0m")
                        return

    print(f"\033[36;1mPassword couldn't be found!\033[0m")


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='JTR on Golem network')
    my_parser.add_argument('--password',
                       '-p',
                       required=True,
                       type=str,
                       help='Password to crack')
    my_parser.add_argument('--num_nodes',
                       '-n',
                       type=int,
                       default=2,
                       help='Number of worker nodes')
    my_parser.add_argument('--timeout',
                       '-t',
                       type=int,
                       default=5,
                       help='Timeout(seconds) for stopping JtR')
    args = my_parser.parse_args()


    if args.num_nodes < 2:
        raise Exception("\033[36;1mNumber of nodes must be greater than one\033[0m")
    print(f"\033[36;1mStart processing JtR on Golem using:\n Password = {args.password}, Timeout(seconds): {args.timeout}s\033[0m")
    print(f"\033[36;1mNumber of worker nodes: {args.num_nodes}\033[0m")

    enable_default_logger()
    loop = asyncio.get_event_loop()
    task = loop.create_task(main(num_nodes=args.num_nodes, password=args.password, timeout=int(args.timeout)))
    try:
        asyncio.get_event_loop().run_until_complete(task)

    except (Exception, KeyboardInterrupt) as e:
        print(e)
        task.cancel()
        asyncio.get_event_loop().run_until_complete(task)

