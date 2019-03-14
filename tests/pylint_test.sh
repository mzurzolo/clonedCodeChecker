#!/bin/bash

pylint --rcfile=$CCC_ENV/.pylint.cfg $CCC_ENV/clonedcodechecker > $CCC_ENV/pylint.log
