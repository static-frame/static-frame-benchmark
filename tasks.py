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



@invoke.task
def benchtest(context):
    '''Clean doc and build artifacts
    '''
    context.run('asv dev')



@invoke.task
def bench08(context):
    '''Clean doc and build artifacts
    '''
    context.run('asv run v0.8.18..master --skip-existing')


@invoke.task
def publish(context):
    context.run('asv publish')

@invoke.task
def preview(context):
    context.run('asv preview')

@invoke.task(pre=(bench08, publish, preview))
def bpp(context):
    '''bench, publihs, preview
    '''
    pass

