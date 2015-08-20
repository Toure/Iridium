# Iridium
Openstack Functional Test Framework.

### Introduction

What's missing from Openstack QE / Dev groups? In one phrase “white box testing” or the ability to test individual
functions and subcomponents, this will allow us to uncover small issues in the code base which can lead to larger
problems in the future. This is what is currently missing from many organizations, methods which allow engineers to
perform micro-test or more focused test which insures a more robust product. Iridium looks to fill this gap and become
part of the one major component most testing and development organizations have been needing. A low level functional
product automation for quality engineers non-verse in python and a test library for those experienced to create new
ad-hoc functional test. This focus differentiates Iridium from Tempest and Rally as those two frameworks / testbeds
are aimed at testing a completed solution, or what is better known as End to End scenarios test which is also known
as “black box testing”, this approach is needed to insure that the customer experience is free of external service
fawls, but it does not address issues where code path may not be executed do to the varying configurations which
is possible with OpenStack.
