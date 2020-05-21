#!/bin/bash
celery worker -A capritools -B -c 2
