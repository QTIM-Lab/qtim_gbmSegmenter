
class PipelineStep(object) :

    def __init__(self, input_volume, output_filename, specific_function, parameters):

        self.input_volume = input_volume
        self.output_filename = output_filename
        self.specific_function = specific_function
        self.parameters = parameters

if __name__ == '__main__':
    pass