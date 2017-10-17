###############################################################
# Imports
###############################################################
from System import *
from System.Diagnostics import *
from System.IO import *

from Deadline.Events import *
from Deadline.Scripting import *

import os
import string
#########################################################################################
# This is the function called by Deadline to get an instance of the Draft event listener.
#########################################################################################


def GetDeadlineEventListener():
    return CustomEnvironmentCopyListener()


def CleanupDeadlineEventListener(eventListener):
    eventListener.Cleanup()

###############################################################
# The event listener class.
###############################################################


class CustomEnvironmentCopyListener (DeadlineEventListener):

    def __init__(self):
        self.OnJobSubmittedCallback += self.OnJobSubmitted

    def Cleanup(self):
        del self.OnJobSubmittedCallback

    def OnJobSubmitted( self, job):
        # Only execute for Nuke jobs.
        jobPlugin = job.JobPlugin
        if not job.JobPlugin in ["Nuke", "NukeFrameServer"]:
            return

        print("This is a Nuke Job")
        # List of environment keys you don't want passed.
        unwantedkeys = self.GetConfigEntryWithDefault("UnwantedEnvKeys", "")
        
        wantedkeys = self.GetConfigEntryWithDefault("WantedEnvKeys", "")
        
        usewantedkeys = []

        # Split out on commas, gettting rid of excess whitespace and make uppercase
        #unwantedkeys = [string.upper(x.strip()) for x in unwantedkeys.split(',')]

        #wantedkeys = [string.upper(x.strip()) for x in wantedkeys.split(',')]

        self.LogInfo("Unwanted Environment keys defined as:")
        self.LogInfo(str(unwantedkeys))
        
        self.LogInfo("Wanted Environment keys defined as:")
        self.LogInfo(str(wantedkeys))

        self.LogInfo("On Job Submitted Event Plugin: Custom Environment Copy Started")

        # Go through the current system environment variables not copying the unwanted keys
        for key in os.environ:
            if string.upper(key) in wantedkeys:
                usewantedkeys.append(key)

        # Set chosen variables to job
        for key in usewantedkeys:
            self.LogInfo("Setting %s to %s" % (key, os.environ[key]))
            job.SetJobEnvironmentKeyValue(key, os.environ[key])

        RepositoryUtils.SaveJob(job)

        self.LogInfo("On Job Submitted Event Plugin: Custom Environment Copy Finished")
