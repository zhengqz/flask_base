#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Celery send mail
    Date: 2016/9/22
    Time: 10:52
"""

from __future__ import absolute_import

from apps.common.factory import create_celery_app

celery = create_celery_app()


@celery.task
def send_manger_added_email(*recipients):
    print("sending manager added email...")


@celery.task
def send_manager_removed_email(*recipients):
    print("sending manager removed email...")
