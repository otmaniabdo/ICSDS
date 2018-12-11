import os, sys


class FileSplitterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


def usage():
    return """\nUsage: FileSplitter.py -i <inputfile> -n <chunksize> [option]\n
    Options:\n
    -s, --split  Split file into chunks
    -j, --join   Join chunks back to file.
    """


class FileSplitter:
    """ File splitter class """

    def __init__(self):

        # cache filename
        self.__filename = ''
        # number of equal sized chunks
        self.__numchunks = 2
        # Size of each chunk
        self.__chunksize = 0
        # Optional postfix string for the chunk filename
        self.__postfix = ''
        # Program name
        self.__progname = "FileSplitter.py"
        # Action
        self.__action = 0  # split
        self.filesPart = ["1","2"]

    def parseOptions(self, filename,opt):

        self.__filename = filename
        if opt.lower() == 's':
            self.__action = 0  # split
        elif opt.lower() == 'j':
            self.__action = 1  # combine


    def do_work(self):
        if self.__action == 0:
            return self.split()
        elif self.__action == 1:
            self.combine()
        else:
            return None

    def split(self):
        """ Split the file and save chunks
        to separate files """
        print ('Splitting file', self.__filename)

        try:
            f = open(self.__filename, 'rb')
        except (OSError, IOError) as e:
            raise FileSplitterException(str(e))

        bname = (os.path.split(self.__filename))[1]
        # Get the file size
        fsize = os.path.getsize(self.__filename)
        # Get size of each chunk
        self.__chunksize = int(float(fsize) / float(self.__numchunks))

        chunksz = self.__chunksize
        total_bytes = 0

        for x in range(self.__numchunks):
            chunkfilename = bname + '-' + str(x + 1) + self.__postfix
            self.filesPart[x] = "temp/"+chunkfilename
            # if reading the last section, calculate correct
            # chunk size.
            if x == self.__numchunks - 1:
                chunksz = fsize - total_bytes

            try:
                print ('Writing file', chunkfilename)
                data = f.read(chunksz)
                total_bytes += len(data)
                chunkf = open("temp/"+chunkfilename, 'wb')
                chunkf.write(data)
                chunkf.close()
            except (OSError, IOError) as e:
                print (e)
                continue
            except EOFError as e:
                print (e)
                break

        print('Done.')
        return (self.filesPart)
    def sort_index(self, f1, f2):

        index1 = f1.rfind('-')
        index2 = f2.rfind('-')

        if index1 != -1 and index2 != -1:
            i1 = int(f1[index1:len(f1)])
            i2 = int(f2[index2:len(f2)])
            return i2 - i1

    def combine(self, part1, part2):

        chunkfiles = []
        chunkfiles.append(part1)
        chunkfiles.append(part2)

        data = ''
        bname = part1.replace('-1','')
        print (bname)
        for f in chunkfiles:

            try:
                print('Appending chunk : ',f)
                data += open(f, 'rb').read()
            except (OSError, IOError, EOFError) as e:
                print (e)
                continue

        try:
            f = open(bname, 'wb')
            f.write(data)
            f.close()
        except (OSError, IOError, EOFError) as e:
            raise FileSplitterException(str(e))

        print
        'Wrote file', bname


