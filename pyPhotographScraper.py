
import os
import sys
import getopt
import shutil
import time
from exif import Image

EXT_TYPE = 0
MOVE_TYPE = 1
SCR_DIR = 2
DEST_DIR = 3
EXIF_ONLY = 4

COPY = 0
MOVE = 1

REPORT_NAME = "_report.txt"

JPEG = '.jpg'

ignoreDirKeyWords = [
    'Recycle',
    'Windows',
    'System Volume Information',
    'AppData'
]


def argumentExtraction(argv):
    destFile = None
    srcFile = None
    extType = None
    moveType = None
    exifOnly = True

    try:
        [opts, argv] = getopt.getopt(argv, "ht:s:d:cmz", [
                                     "help", "type=", "srcfile=", "destfile=", "copy", "move", "all"])
    except getopt.GetoptError:
        helpPrints()
        return None
    for opt, arg in opts:
        if opt == '-h':
            helpPrints()
            exit()
        elif opt in ("-t", "--type"):
            extType = arg.split(' ')
            print('File type is {0}'.format(extType))
        elif opt in ("-s", "--srcfile"):
            srcFile = arg
            print("Source Directory is {0}".format(srcFile))
        elif opt in ("-d", "--destfile"):
            destFile = arg
            print("Destination Directory is {0}".format(destFile))
        elif opt in ("-c", "--copy"):
            moveType = COPY
            print('Copy the files from {0} to {1}'.format(srcFile, destFile))
        elif opt in ("-m", "--move"):
            moveType = MOVE
            print('Move the files from {0} to {1}'.format(srcFile, destFile))
        elif opt in ("-z", "--all"):
            exifOnly = False
            print('Include all {0} types'.format(extType))

    return [extType, moveType, srcFile, destFile, exifOnly]


def helpPrints():
    print('\npyScraper.py <arguments> \n')
    print('~~~ARGUMENT LIST~~~\n')
    print('-t:\tfile extension to be moved/copied\t-t <type>\n')
    print('-s:\tSource Directory\t-s <srcpath>\n')
    print('-d:\tDestination Path\t-d <destpath>\n')
    print('-c:\tCopy the file to the destination\n')
    print('-m:\tMove the file from the source to the destination\n')


def main(argv):

    scraperParams = argumentExtraction(argv)
    if(scraperParams != None):
        scraper(scraperParams)


def scraper(scraperParams):
    fileMoved = 0
    has_exif = False

    reportFile = open(os.path.join(scraperParams[DEST_DIR], REPORT_NAME), "w+")

    startTime = time.time()

    for root, _, files in os.walk(scraperParams[SCR_DIR], topdown=True):
        ignoreDir = any(word for word in ignoreDirKeyWords if word in root)
        if(ignoreDir == False):
            print("root directory: {0}".format(root))
            for filename in files:
                print("filename: {0}".format(filename))
                _, extension = os.path.splitext(filename)

                extensionExists = extension.lower() in scraperParams[EXT_TYPE]
                if extensionExists:
                    moveFile = os.path.join(root, filename)
                    with open(moveFile, 'rb') as open_file:
                        if(extension.lower() == JPEG):
                            image_file = Image(open_file)

                            if(image_file.has_exif == True):
                                has_exif = True
                                if(hasattr(image_file, 'make')):
                                    make = image_file.make.replace(" ", "_")
                                    makeDir = os.path.join(
                                        scraperParams[DEST_DIR], make)
                                    if not os.path.exists(makeDir):
                                        os.mkdir(makeDir)
                                    destDir = makeDir
                                else:
                                    make = 'unknown'
                                    makeDir = os.path.join(
                                        scraperParams[DEST_DIR], make)
                                    if not os.path.exists(makeDir):
                                        os.mkdir(makeDir)
                                    destDir = makeDir

                                if(hasattr(image_file, 'model')):
                                    model = image_file.model.replace(" ", "_")
                                    modelDir = os.path.join(makeDir, model)
                                    if not os.path.exists(modelDir):
                                        os.mkdir(modelDir)
                                    destDir = modelDir

                                if(hasattr(image_file, 'datetime')):
                                    fileNewName = image_file.datetime.replace(
                                        " ", "_").replace(":", "_") + extension
                                else:
                                    fileNewName = filename
                                destDir = os.path.join(destDir, fileNewName)

                            elif(scraperParams[EXIF_ONLY] == False):
                                make = 'unknown'
                                makeDir = os.path.join(
                                    scraperParams[DEST_DIR], make)
                                if not os.path.exists(makeDir):
                                    os.mkdir(makeDir)
                                destDir = os.path.join(makeDir, filename)
                        else:
                            make = 'unknown'
                            makeDir = os.path.join(
                                scraperParams[DEST_DIR], make)
                            if not os.path.exists(makeDir):
                                os.mkdir(makeDir)
                            destDir = os.path.join(makeDir, filename)

                    if(has_exif == True or scraperParams[EXIF_ONLY] == False):
                        if(scraperParams[MOVE_TYPE] == COPY):
                            print('copy file {0}'.format(moveFile))
                            try:
                                dest = shutil.copy2(moveFile, destDir)
                                print('file copied to {0}'.format(dest))
                                reportFile.write(
                                    '{0}\t--->\t{1}\n'.format(moveFile, dest))
                                fileMoved += 1
                            except:
                                print(
                                    'FAILED to copy file {0}'.format(moveFile))
                        elif(scraperParams[MOVE_TYPE] == MOVE):
                            print('move file {0}'.format(moveFile))
                            try:
                                dest = shutil.move(moveFile, destDir)
                                print('file moved to {0}'.format(dest))
                                reportFile.write(
                                    '{0}\t--->\t{1}\n'.format(moveFile, dest))
                                fileMoved += 1
                            except:
                                print(
                                    'FAILED to move file {0}'.format(moveFile))
                    has_exif = False

    reportFile.close()
    endTime = time.time()
    totalTime = endTime - startTime
    print("Time Taken: {0} seconds".format(totalTime))
    print("Total Files Moved: {0}".format(fileMoved))


if __name__ == "__main__":
    main(sys.argv[1:])
