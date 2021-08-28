import sys
import os
import typing as tp

import invoke

#-------------------------------------------------------------------------------

@invoke.task
def clean(context):
    '''Clean doc and build artifacts
    '''
    context.run('rm -rf .asv')
    context.run('rm -rf .pytest_cache')
    context.run('rm -rf docs')


