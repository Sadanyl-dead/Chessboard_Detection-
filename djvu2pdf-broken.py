import os
import sys
import time
import _thread

# author: ~/angeloped

stat = []


def convrt(fpath, fname):
    print("converting \"{0}/{1}\"....".format(fpath, fname))
    os.system("djvups \"{0}/{1}\" | ps2pdf - \"{0}/pdfied/{2}\"".format(
        fpath, fname, fname.replace(".djvu", ".pdf")))
    stat.pop()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        fpath = os.getcwd()
    elif len(sys.argv) <= 3:
        buff_limit = int(sys.argv[2]) if len(sys.argv) == 3 else 6

        if os.path.exists(sys.argv[1]):
            fpath = sys.argv[1]
        else:
            print("target path not found.. setting './' as cwd.")
            fpath = os.getcwd()
    else:
        print("simple usage: python djvu2pdf.py <path/> <buff 'default:6'>")

    if not os.path.exists("{0}/pdfied".format(fpath)):
        os.mkdir("{0}/pdfied".format(fpath))

    for fname in os.listdir(fpath):
        while len(stat) == buff_limit:  # process limiter
            time.sleep(1)

        if fname[-5:] == ".djvu":
            _thread.start_new_thread(convrt, (fpath, fname,))
            stat.append("")

    while bool(stat):
        time.sleep(1)
