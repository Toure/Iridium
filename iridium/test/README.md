## Test repository layout.
The current layout should not be changed, the packages described illustrates how test should be
structured. This is due to how the test runner will examine the requested test based on packages in which
each test is requested.

> nova_tests will contain all test pertaining to nova.

Directory Structure:
```
|-- test/
|   |--cinder_tests
|   |--glance_tests
|   |--nova_tests/
|   |  |--sanity_test.py
|   |  |--numa_test.py
|   |  |--instances_test.py
```
