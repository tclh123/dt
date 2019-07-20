# DT

DT is a distributed system testing framework for cloud native.

The idea is to design a long running service.
Users can choose a test suite to run, that against a distributed system which installed by helm chart to a k8s cluster.
The service collect test suite's records and distributed system's metrics and display to its web dashboard.

It should be easy to add a new testing object and test suites to this framework.
Just write a chart yaml describe the chart about the source to download helm charts and values, and extra k8s crd, rbac yamls to apply.

See [dtcharts](dtcharts/) to learn how to write a chart yaml.
See [dtsuite](dtsuite/) to learn how to write a test suite. Usually you only need to override a defined Model that the framework provided.

The test suite driver will choose to run each test function of a test suite at a configurable probability and rate.
It will also send chaos monkeys to the cluster. Test suite can defined its own chaos monkeys as well.

Chaos is done in the usual way, like stop a pod, or insert iptables rules to simulate a network partition, or use tc(traffic control) to limit network throughput.

## Status

Currently this is just a toy to prove the idea. Many features are not implemented. Don't waste your time on this.

## Install

Only tested under python3.7

```bash
git clone https://github.com/tclh123/dt
cd dt
pip install .
```
Or create a virtual environment,

```bash
git clone https://github.com/tclh123/dt
cd dt
make init
source venv/bin/activate
```

## Usage

Currenty it only provides a CLI as an entry point, called `dt`, ~~which in chinese pronounced like eggache~~

```bash
# see help message
dt -h

# list charts
dt list chart

# list suites
dt list suite

# run a test suite
dt run redis -t 10 -d
```

## Suite

A suite yaml looks like,

```yaml
name: redis
chart: redis
testcase_cls: 'dt.common.suite.impl.bank:BankTestCase'
testcase_model_cls: 'dtsuite.redis.bank:Bank'
values:
  clusterDomain: __CLUSTER_DOMAIN__
```

## Testing

As the object being tested is a concurrent system, and it's a black box.
We can't just send another call to expect a determinate value after we do some operation, because the value may have been changed by other concurrent operations.
At meanwhile, you can't tell the exact time of the operation been executed on the server, because the request sent later may arrive first through the network.

It uses [porcupine](https://github.com/anishathalye/porcupine) as the linearizability checker.
