

class MetadataParser:
    num_classes = None

    train_start = None
    train_end   = None

    val_start   = None
    val_end     = None

    test_start  = None
    test_end    = None

    all_exludes = []


    def __init__(self):
        pass

    def parse(self, metadata_path):
        '''
        Parse the file, load into the class.

        Arbitrary to call. Calling this will optimize code by reducing disk access.
        '''
        db_file  = open(metadata_path, 'r')

        lines = list(map(lambda x: x.split('#')[0].splitlines()[0], db_file.readlines()))

        self.num_classes = int(lines[0])

        self.train_start = int(lines[2])
        self.train_end   = int(lines[3])

        self.val_start   = int(lines[5])
        self.val_end     = int(lines[6])

        self.test_start  = int(lines[8])
        self.test_end    = int(lines[9])

        self.all_exludes = []

        if len(lines) > 10:
            if lines[10] == 'Excluded':
                num_excludes = int(lines[11])
                self.all_exludes  = [int(lines[12+x]) for x in range(num_excludes)]


    def get_value(self, value_name, metadata_path=None):
        '''
        Get value by its name. Name is supplied as string.


        Note: metadata_path will override current class values!
        Example:
            get_value('num_classes')
            get_value('num_classes', 'metadata/1.txt')
        '''

        if metadata_path is None:
            if self.num_classes is None:
                raise FileNotFoundError('No metadata filename is given nor saved in the database')
        else:
            self.parse(metadata_path)

        if value_name == 'num_classes':
            return self.num_classes
        elif value_name == 'train_start':
            return self.train_start
        elif value_name == 'train_end':
            return self.train_end
        elif value_name == 'val_start':
            return self.val_start
        elif value_name == 'val_end':
            return self.val_end
        elif value_name == 'test_start':
            return self.test_start
        elif value_name == 'test_end':
            return self.test_end
        elif value_name == 'all_exludes':
            return self.all_exludes
        else:
            raise ValueError('Unsupported value requested ' + str(value_name))
