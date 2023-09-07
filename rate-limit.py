#!/usr/bin/env python3
"""
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
from googleapiclient import discovery
from google.oauth2 import service_account
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

sid = {
    "serviceIds": ["appengine.googleapis.com",
                          "recommender.googleapis.com",
                          "sqladmin.googleapis.com",
                   "apikeys.googleapis.com",
                   "iam.googleapis.com",
                   "cloudresourcemanager.googleapis.com",
                   "orgpolicy.googleapis.com",
                   "cloudasset.googleapis.com",
                   "accessapproval.googleapis.com",
                   "essentialcontacts.googleapis.com"
                   ]
}


def enable_apis(projectId, credentials, serviceids):
    logger.info('Enabling api for project %s', projectId)
    try:
        credentials = credentials.with_quota_project(projectId)
        service = discovery.build('serviceusage', 'v1', credentials=credentials)
        request = service.services().batchEnable(parent="projects/" + projectId, body=serviceids)
        request.execute()
        logger.info('Api enablement for project %s successful', projectId)
        logger.info('Apis enabled are %s', sid.get('serviceIds'))
    except Exception as e:
        logger.error('Failed to enable api for project %s error is %s', projectId, str(e))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service_account_json_filepath', action='store', type=str, required=True,
                        help='Provide service account json file path')
    args = parser.parse_args()
    try:
        credentials = service_account.Credentials.from_service_account_file(args.service_account_json_filepath)
        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
        request = service.projects().list()
        while request is not None:
            response = request.execute()

            for project in response.get('projects', []):
                enable_apis(project['projectId'], credentials, sid)
            request = service.projects().list_next(previous_request=request, previous_response=response)
    except Exception as e:
        logger.error("Unable to load projects accessible via service account, error is %s", str(e))


if __name__ == "__main__":
    main()
