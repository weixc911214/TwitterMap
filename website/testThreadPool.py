__author__ = 'wei'
# -*- coding:utf-8 -*-
__author__ = 'wei'

import Queue
import threading
import time

class WorkManager(object):
    def __init__(self, job, work_num = 1000, thread_num = 2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.job = job
        self.__init_work_queue(work_num, self.job)
        self.__init_thread_pool(thread_num)


    '''
    初始化线程池
    '''
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))



    '''
    初始化工作队列
    '''
    def __init_work_queue(self, work_num, func):
        for i in range(work_num):
            self.add_job(self.job, i)
    '''
    添加一项工作入队
    '''
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    '''
    检查剩余队列任务
    '''
    def check_queue(self):
        return self.work_queue.qsize()

    '''
    等待所有线程运行完毕
    '''
    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class Work(threading.Thread):

    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()
    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block = False)
                do(args)
                self.work_queue.task_done()
            except Exception, e:
                print str(e)
                break


work = WorkManager(Work)
