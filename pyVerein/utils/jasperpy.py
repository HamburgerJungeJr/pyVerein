from pyreportjasper import JasperPy as JaspPy
from pyreportjasper.jasperpy import FORMATS
import os
import subprocess

class JasperPy(JaspPy):
    def execute(self, run_as_user=False):
        if run_as_user and (not self.windows):
            self._command = 'su -u ' + run_as_user + " -c \"" + \
                               self.command + "\""

        if os.path.isdir(self.path_executable):
            try:
                output = subprocess.run(
                    self.command, shell=True, check=True, encoding='utf-8', stderr=subprocess.PIPE)
            except AttributeError:
                output = subprocess.check_call(self.command, shell=True)
            except subprocess.CalledProcessError as e:
                raise NameError('Your report has an error and couldn\'t be processed!\n' + e.stderr)
        else:
            raise NameError('Invalid resource directory!')

        return output.returncode