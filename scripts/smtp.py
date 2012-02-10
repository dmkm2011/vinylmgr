from datetime import datetime
import asyncore
from smtpd import SMTPServer

class EmlServer(SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'), self.no)
        f = open(filename, 'w')
        f.write(data)
        f.close()
        print '%s saved.' % filename
        self.no += 1


def run():
    foo = EmlServer(('localhost', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':

    from os.path import exists, join
    from os import mkdir, chdir, getcwd

    target_directory = join( getcwd(), "emails" )
    if exists(target_directory):
        chdir(target_directory)
    else:
        try:
            mkdir(target_directory)
        except OSError:
            from sys import exit
            exit("The containing folder couldn't be created, check your permissions.")
        chdir(target_directory)
    print "Using directory %s" % target_directory

    run()
