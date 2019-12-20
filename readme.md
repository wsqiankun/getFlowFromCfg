# basic config
"TEST_CONFIG" and "mysql" are two basic configurations,
which specifies the test type and mysql server infomations.

[TEST_CONFIG]
test_type=rdt_endurance
first_step=step_1
loop=1

[mysql]
host=10.0.0.10
user=root
passwd=MYsql123
database=testlog

## TEST_CONFIG
test_type  can be choosen from [rdt_endurance, rdt_quality, self_config]
first_step assign the fisrt test item
loop       assign the main cycle loop times

## mysql
this sections tells test script the mysql server infomations

# test item

[step_1]
test_type=single
first_step=""
test_name=seq_rw
test_loop=1
next_step=step_2 

section name "step_1" is the test lable, name it  in any style is ok
test_type     can be choosen from [single, group], single means a single test script, 
              group mean a combination of group or single item
test_name     is also the test case dir and test case script name(test_name/test_name.py)
test_loop     current item loop times
first_step    if item type is group, first_step mean the first step of the group
next_step     the group or signle item next test item

## notice
if the value of first_step and next_step, this means this item is the last item of the test 