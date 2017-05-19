import os
from ompdal import OMPDAL, OMPSettings, OMPItem
ompdal = OMPDAL(db, myconf)
import gluon.contrib.simplejson as sj


# http://localhost:8000/omp_rest/api/files/230?submissionId=43
def files():
    if request.args and request.vars.get("submissionId"):
        sf = db.submission_files
        s_id = request.vars.get("submissionId")
        q = ((sf.file_id == request.args[0]) & (sf.submission_id == s_id))
        f = db(q).select(sf.ALL).first()
        f_name = '{}-{}-{}-{}-{}-{}.{}'.format(f['submission_id'], f['genre_id'], f['file_id'], f['revision'], f[
                                               'file_stage'], str(f['date_uploaded']).replace('-', '')[:8], f['file_type'].split('/')[1]) if f else 'not found'
        s = ompdal.getSubmission(s_id)
        f_path = os.path.join(request.folder, 'static', 'files', 'presses', str(
            s['context_id']), 'monographs', s_id, 'submission', 'proof', f_name)
        try:
            fh = open(f_path, 'rb')
            return response.stream(fh)
        except:
            raise HTTP(401, '{} {}'.format(f_path, 'not found'))

    else:
        raise HTTP(401, 'required {fileId}/submissionId={submissionId}')

    return


# https://localhost:8000/omp_rest/api/backend/submissions
def backend():
    if request.args[0] == 'submissions':
        pr = ompdal.getPresses()
        ps = [i['press_id'] for i in pr]
        r = []

        for p in ps:
            for j in ompdal.getSubmissionsByPress(p, status=1):
                r.append(j['submission_id'])
        return sj.dumps(r)

    else:
        raise HTTP(401, 'required backend/submissions')
    return


# https://localhost:8000/omp_rest/api/submissions/43
def submissions():
    fs = []
    if request.args:
        s = request.args[0]
        if s.isdigit():
            for cs in ompdal.getChaptersBySubmission(s):
                for pf in ompdal.getDigitalPublicationFormats(s, available=True, approved=True):
                    f = ompdal.getLatestRevisionOfChapterFileByPublicationFormat(
                        cs['chapter_id'], pf['publication_format_id'])
                    if f:
                        fs.append(f['file_id'])
            return sj.dumps(fs)

        else:
            raise HTTP(401, 'required submissions/{submissionId}')
    else:
        raise HTTP(401, 'required submissions/{submissionId}')
    return
