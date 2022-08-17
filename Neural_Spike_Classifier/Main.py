import random
import scipy.io as spio
import scipy.special
from scipy.signal import find_peaks, butter, savgol_filter, sosfiltfilt
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import time
import os

#Go to line 441 for User inputs

#Method 1 Neural Network adapted from coursework A
class NeuralNetwork:
    # Init the network, this gets run whenever we make a new instance of this class
    def __init__ (self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set the number of nodes in each input, hidden and output layer
        self.i_nodes = input_nodes
        self.h_nodes = hidden_nodes
        self.o_nodes = output_nodes
        # Weight matrices, wih (input -> hidden) and who (hidden -> output)
        self.wih = np.random.normal(0.0, pow(self.h_nodes, -0.5), (self.h_nodes, self.i_nodes))
        self.who = np.random.normal(0.0, pow(self.o_nodes, -0.5), (self.o_nodes, self.h_nodes))
        # Set the learning rate
        self.lr = learning_rate
        # Set the activation function, the logistic sigmoid
        self.activation_function = lambda x: scipy.special.expit(x)
        # Train the network using back-propagation of errors
    def train(self, inputs_list, targets_list):
        # Convert inputs into 2D arrays
        inputs_array = np.array(inputs_list, ndmin=2).T
        targets_array = np.array(targets_list, ndmin=2).T
        # Calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs_array)
        # Calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # Calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # Calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        # Current error is (target - actual)
        output_errors = targets_array - final_outputs
        self.output_errors = output_errors
        # Hidden layer errors are the output errors, split by the weights, recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors)
        # Update the weights for the links between the hidden and output layers
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)),
        np.transpose(hidden_outputs))
        # Update the weights for the links between the input and hidden layers
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
        np.transpose(inputs_array))
        # Query the network
    def query(self, inputs_list):
        # Convert the inputs list into a 2D array
        inputs_array = np.array(inputs_list, ndmin=2).T
        # Calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs_array)
        # Calculate output from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        # Calculate signals into final layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # Calculate outputs from the final layer
        final_outputs =self.activation_function(final_inputs)
        return final_outputs

    def predict(self, sub_spikes):
        # Used to dcreate the predictions of submission dataset classes
        idx = 0
        prediction = []
        for spike in sub_spikes:
            # Query each spike into the neural network
            out = self.query(spike)
            label = np.argmax(out) + 1
            idx += 1
            # Append Results to output array
            prediction.append(label)

        return prediction

    def run(self,full_spikes, neuron_classes, iterations, training_proportion ):
        # This function sets up and run iteration loop for neural net training
        # Start the timer
        time_start = time.time()
        output_nodes = 5
        # Start counter
        a = 0
        # Split data into separate training and validation sets, based on given proportion
        training_data = full_spikes[0:(int(len(full_spikes) * training_proportion))]
        validation_data = full_spikes[((int(len(full_spikes) * training_proportion))):]
        test_targets = neuron_classes[((int(len(full_spikes) * training_proportion))):]
        while a < iterations:
            a += 1
            # Print iteration to monitor progress
            print(a)
            # Index counter
            idx = 0
            for spike in training_data:
                # Create target array for each spike, with 0.99 as the correct class
                targets = np.zeros(output_nodes) + 0.01
                targets[neuron_classes[idx] - 1] = 0.99
                idx += 1
                self.train(spike, targets)
        idx = 0
        # Initiate prediction array
        prediction = []
        #Validation phase
        for spike in validation_data:
            # Query each validation spike
            out = self.query(spike)
            #Find label output
            label = np.argmax(out) + 1
            idx += 1
            #Append label to output array
        # Stop timer
        time_end = time.time()
        time_elapsed = time_end-time_start
        print(time_elapsed)
        # Generate performance metrics for each class, including  precision, recall F1 score and accuracy
        performance_metrics = metrics.classification_report(test_targets, prediction, digits=4)
        # Generate confusion matrix
        c_matrix = metrics.confusion_matrix(test_targets, prediction)
        # print to console for viewing
        print(c_matrix)
        print(performance_metrics)


#Method 2, K-Nearest Neighbor
class KNearestNeighbor:
    def __init__(self,spikes,labels, train_proportion = 0.8):
        self.time_start = time.time()
        #Split spikes and labels into training and validation data based on given proportion
        self.train_spikes = spikes[:int(len(spikes)*train_proportion)]
        self.test_spikes = spikes[int(len(spikes)*train_proportion):]
        self.train_labels = labels[:int(len(spikes)*train_proportion)]
        self.test_labels = labels[int(len(spikes)*train_proportion):]

    def create_model(self,k_neighbors,p_distance):
        # Generate the KNN model using the scikit-learn library
        # Instantiate KNeighborsClassifier Class
        self.model = KNeighborsClassifier(n_neighbors=int(k_neighbors), p=p_distance)
        self.model.fit(self.train_spikes, self.train_labels)
        """Fit the k-nearest neighbors classifier from the training dataset.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features) or \
                (n_samples, n_samples) if metric='precomputed'
            Training data.
        y : {array-like, sparse matrix} of shape (n_samples,) or \
                (n_samples, n_outputs)
            Target values.
        Returns
        -------
        self : KNeighborsClassifier
            The fitted k-nearest neighbors classifier.
        """

    def score(self):
        # Predict using knn model
        self.prediction = self.model.predict(self.test_spikes)
        # Calculate accuracy score
        self.accuracy = metrics.accuracy_score(self.test_labels, self.prediction)
        # End Timer
        self.time_end = time.time()
        time_elapsed = self.time_end - self.time_start
        print(time_elapsed)
        # Generate performance metrics for each class, including  precision, recall F1 score and accuracy
        performance_metrics = metrics.classification_report(self.test_labels, self.prediction, digits=4)
        print(performance_metrics)
        # Generate confusion matrix
        c_matrix = metrics.confusion_matrix(self.test_labels, self.prediction)
        print(c_matrix)

    def predict(self, submission_data):
        #Generate predictions for submission classes using knn model
        self.prediction = self.model.predict(submission_data.full_spikes)
        return self.prediction

#Handle Data using this class
class DataSet:
    def __init__(self, data_points, labels = 0, labels_idx = 0, type = 'submission'):
        # Assign inputs to self for easy access
        self.signal = data_points
        self.all_labels = labels
        self.all_labels_idx = labels_idx
        self.type = type

    def sort_spikes(self):
        # Put spike labels and indices into chronological order
        sorted_args = np.argsort(self.all_labels_idx)
        self.all_labels_idx = self.all_labels_idx[sorted_args]
        self.all_labels = self.all_labels[sorted_args]

    def filter_signal(self, butter_order = 3, fc_low = 30, fc_high =1900, savgol_window = 19, savgol_order = 5):
        # This function handles all signal filtering for training and submission data sets
        # Always starts with a high pass butter filter
        sos = butter(butter_order, fc_low, btype='high', analog=False, output='sos', fs=25000)
        # Apply filter forwards and backwards using sosfiltfilt
        filtered_signal1 = sosfiltfilt(sos, self.signal)
        # Different options of 2nd filters for submission and training data sets due to different noise profiles
        if self.type == 'submission':
            # High pass butter filter
            sos = butter(butter_order, fc_high, btype='low', analog=False, output='sos', fs=25000)
            # Apply filter forwards and backwards using sosfiltfilt
            filtered_signal2 = sosfiltfilt(sos,filtered_signal1)
        if self.type == 'training':
            # choose between savgol or high pass by commenting one out
            # Savgol filter:
            filtered_signal2 = savgol_filter(filtered_signal1, savgol_window, savgol_order)
            # Low pass filter
            #sos = butter(butter_order, fc_high, btype='low', analog=False, output='sos', fs=25000)
            # Apply filter forwards and backwards using sosfiltfilt
            #filtered_signal2 = sosfiltfilt(sos, filtered_signal1)
        # Set filtered signal to self for easy access
        self.filtered_signal = filtered_signal2
        # Plot figure of signal filtering progress
        a = plt.figure()
        a.suptitle('Signal Filtering: '+ str(self.type) + '.mat')
        plt.plot(self.signal, c='b', label = 'Raw Signal')
        plt.plot(filtered_signal1, c='g', label = 'High Pass Butter 30hz')
        plt.plot(filtered_signal2, c = 'r', label = 'Passband Butter: 30hz, 1900hz')
        plt.legend()
        # This will be plotted at the end if plot flag is enabled

    def normalize_data(self):
        # Make values between 0 and 1 for more compatibility with machine learning
        self.normal_signal = self.filtered_signal - self.filtered_signal.min()
        self.normal_signal = self.filtered_signal / self.filtered_signal.max()
        self.normal_signal = (self.normal_signal * 0.99) + 0.009


    def detect_spikes(self, window, prom):
        # Use fine_peaks function for peak detection
        # Different peak thresholds for submission and trainging sets due to different noise profile
        if self.type == 'submission':
            self.threshold = 1.35*np.std(self.filtered_signal)
        if self.type == 'training':
            self.threshold = np.std(self.filtered_signal)
            # Find peak indices and heights
        peak_indices, peak_height = find_peaks(self.filtered_signal, height=(self.threshold),
                                               prominence=prom)  # need prominence to prevent small sub-spikes on spike from being detected
        print('peaks found:' + str(len(peak_indices)))
        # Initiate output lists
        self.full_spikes = []
        self.neuron_classes = []
        self.neuron_index = []
        self.duplicates = []
        self.normalize_data()
        # Separate process for trainging and submission data sets
        if self.type == 'training':
            # loop through each peak
            for detected_index in peak_indices:
                # find corresponding index in training data
                i = self.all_labels_idx[self.all_labels_idx < detected_index].max()
                # Detect duplicates and note them into duplicates list
                if i in self.neuron_index:
                    self.duplicates.append(i)
                else:
                    # find neuron class
                    neuron_class = self.all_labels[np.where(self.all_labels_idx == i)[0]]
                    # Create window for spike
                    full_spike = self.normal_signal[detected_index - window[0]:detected_index + window[1]]
                    # append results
                    self.full_spikes.append(full_spike)
                    self.neuron_classes.extend(neuron_class)
                    self.neuron_index.append(i)
        if self.type == 'submission':
            #The same process is used for submission, but without the associating with class phase.
            for detected_index in peak_indices:
                # Create window for spike
                full_spike = self.normal_signal[detected_index - window[0]:detected_index + window[1]]
                self.full_spikes.append(full_spike)
                self.neuron_index.append(detected_index)
        # Plot duplicates to troubleshoot, if they do exist
        plt.scatter(self.duplicates,self.filtered_signal[self.duplicates], c='r', linewidths=10)
        plt.figure()
        # spike window plot
        plt.suptitle('Peak whiskers for ' + str(self.type) +'.mat')
        plt.scatter(peak_indices,self.filtered_signal[peak_indices], c='r', linewidths=2)
        #Create vertical window whiskers
        for index in peak_indices:
            plt.axvline(x=index-window[0], c='r', linestyle = 'dotted', alpha = 0.7)
            plt.axvline(x=index + window[1], c='r', linestyle = 'dotted', alpha = 0.7)
        plt.plot(self.filtered_signal, c = 'g')
        print('Duplicate peaks:' + str(len(self.duplicates)))

        #plt.show()

    def plot_signal(self,d):
        #Simple plot function
        plt.axhline(y=self.threshold, color='r', linestyle='-')
        plt.plot(d)
        plt.show()

    def signal_noise_ratio(self,s):
        #Calculates signal-to-noise ratio, used during filter tuning
        s = np.asanyarray(s)
        mean = s.mean(0)
        std = s.std(axis=0, ddof=0)
        print(np.where(std == 0, 0, mean / std))

    def analyse_detected_peaks(self):
        # Detect, count and plot which peaks are missing from the 'neuron_index' array of detected spikes
        self.missing_index = []
        # Scan through all labels for ones that do not exist in the detected neurons index
        for idx in self.all_labels_idx:
            exists = idx in self.neuron_index
            if exists == False:
                self.missing_index.append(idx)
        #Get total missing spikes to inform user in console
        self.total_missing_spikes = len(self.missing_index)
        print('There are ' + str(len(self.missing_index)) + ' missing spikes from training data!')
        missing_args = []
        #See which classes these missing spikes belong to
        for index in self.missing_index:
            missing_args.extend(list(np.where(self.all_labels_idx == index)[0]))
        # Pack these classes into a dictionary and print it
        missing_classes = np.array(self.all_labels[missing_args])
        unique, counts = np.unique(missing_classes, return_counts=True)
        print('Missing classes count:')
        print(dict(zip(unique, counts)))
        # Calculate detection percentage, to be used to calculate overall accuracy
        detection_percent = (len(self.all_labels)-len(missing_args))/len(self.all_labels)
        print('Peak detection Percentage: ' + str(detection_percent))
        # Plot missing peaks on the signal graph
        b = plt.figure()
        b.suptitle('Missing Peaks')
        plt.scatter(self.missing_index, self.normal_signal[self.missing_index], c='r')
        plt.plot(self.normal_signal, alpha = 0.5)


class logdata:
    #Class used for logging data to a scv file
    filecount = 0
    # initiate path with file directory for saving csv
    def __init__(self,path):
        self.PATH = path
        if not os.path.exists(path):
            os.makedirs(path)
        now_time = time.localtime()
        # Label file with time start to ensure uniqueness
        self.timestart = ("%02d_%02d_%02d_%02d_%02d_%02d" %(now_time[3],now_time[4],now_time[5],now_time[2],now_time[1],now_time[0]))
        result_file = open(self.PATH + "\\Results_%s.txt" %(self.timestart), "w")
        result_file.close()

    def write(self,input):
        # Write data to .txt file
        result_file = open(self.PATH + "\\Results_%s.txt" %(self.timestart), "a")
        result_file.write(input)
        result_file.close()


class SimulatedAnnealing:
    def __init__(self, first_params, iterations, alpha, training_spikes, training_classes, test_proportion = 0.7,demand = 1.0):
        #Assign inputs to self for easy access
        self.T = 1
        self.T_min = 0.001
        self.demand = demand
        self.iterations = iterations
        self.alpha = alpha
        self.old_params = first_params
        self.training_classes = training_classes
        self.test_proportion = test_proportion
        #use PCA to speed up process at the cost of performance
        pca = PCA(n_components=0.99)
        self.training_spikes = pca.fit_transform(training_spikes)


    def diff(self, params):
        # Input parameters into KNN model
        self.k = int(params[0])
        self.p = int(params[1])
        knn = KNearestNeighbor(self.training_spikes,self.training_classes, self.test_proportion)
        knn.create_model(self.k,self.p)
        knn.score()
        # Calculate the difference between results and target demand
        diff = self.demand - knn.accuracy
        return  diff


    def neighbour(self, params):
        # Change parameters to a neighboring value
        # Since only integers were allowed, te detla function was modified to select
        # a random integer instead of multiplying
        delta = np.random.randint(3) - 1
        params[0] += delta
        params[1] = int(np.random.randint(1,4))
        # Make sure that k does not reach 0
        if params[0] < 0.5:
            params[0] = 1
        return params

    def metropolis_acceptance(self):
        # Calculate the metropolis acceptance threshold, based on the difference
        # Between the ew and old results, and the current annealing temperature
        return np.exp((self.old_diff-self.new_diff)/self.T)

    def anneal(self):
        # Run the annealing loop
        # Reset old_diff
        self.old_diff = self.diff(self.old_params)
        self.diff_values = []
        #Append array to keep track of diff history
        self.diff_values.append(self.old_diff)
        # While loop for the cooling of T to below a threshold
        while self.T > self.T_min:
            i = 1
            # Iterations between each cooling step
            while i <= self.iterations:
                # FInd new parameters amd corresponding diff
                self.new_params = self.neighbour(self.old_params)
                self.new_diff = self.diff(self.new_params)
                # Calculate metropolis acceptance
                ma = self.metropolis_acceptance()
                # Check if metropolis acceptance applies
                if (self.new_diff<self.old_diff) or (ma > random.random()):
                    self.old_params = self.new_params
                    self.old_diff = self.new_diff

                i =+ 1
                #Print to monitor progress
                print(self.T)
                print(i)
                print(self.old_params)
                # Append diff to log history
                self.diff_values.append(self.old_diff)
            #Cool temperature before next loop

            self.T = self.T * self.alpha
        print(self.diff_values)
        return self.old_params

def knn_grid_selection(max_k,max_p):
    # Run grid selection loop for KNN
    # Create lists of parameter combinations
    k_list = np.arange(1,max_k+1)
    p_list = np.arange(1,max_p+1)
    # Create empty array to input results into for accuracy and standard deviation
    result_accuracy = np.zeros((max_k+1,max_p+1))
    result_std = np.zeros((max_k+1,max_p+1))
    # Create results file to save to csv
    results_file_headers = 'k, p, accuracy, standard deviation'
    resultsfile = logdata('C:\PythonProject\CompInt\CourseworkC')
    resultsfile.write(results_file_headers)
    # Run through all combinations
    for k in k_list:
        for p in p_list:
            # Apply parameters to KNN model
            knn = KNearestNeighbor(np.array(training_set.full_spikes), training_set.neuron_classes, 0.98)
            knn.create_model(k, p)
            knn.score()
            # log accuracy results
            result_accuracy[k][p] = knn.accuracy
            # Apply to submission data to find standard deviation of output class totals
            submission_classes = knn.predict(submission_set)
            submission_index = submission_set.neuron_index
            # Zipp results into dictionary
            unique, counts = np.unique(submission_classes, return_counts=True)
            print('Submission Class counts: ')
            print(dict(zip(unique, counts)))
            result_std[k][p] = np.std(counts)
            print('std: ' + str(result_std[k][p]))
            #Write results to csv file
            resultsfile.write('\n' + str(k) + ', ' + str(p) + ', ' + str(knn.accuracy) + ', ' + str(np.std(counts)))
    # mean is always the same once peaks are found


#------------User Inputs-----------#
#Simulated annealing params
alpha = 0.1
iterations = 10
first_params = [np.random.randint(1,20), np.random.randint(1,3)]
first_params = np.array(first_params)
#Neural Network params
hidden_nodes = 1000
learning_rate = 0.05
training_iterations = 50
training_proportion = 0.9
#------------Constants-------------#
sampling_rate = 25000
spike_window = [14,35]
#Function Selection Flags
#Choose only one Machine learning Method
use_NN = False
use_KNN = True
#Optimisation method for KNN
use_SA = False
use_grid_selection = False #Best was accuracy found to be k = 2, p =3, best std was k=3,p=4
#Use Submission data
create_sub = True
#Show Plots
show_plots = False



if __name__ == '__main__':

    #-----Import spike data, class and indices
    training_table = spio.loadmat('training.mat', squeeze_me=True)
    training_data = training_table['d']
    training_class = training_table['Class']
    training_index = training_table['Index']
    submission_data = spio.loadmat('submission.mat', squeeze_me=True)['d']
    unique, counts = np.unique(training_class, return_counts=True)
    print('Training Class counts: ')
    print(dict(zip(unique, counts)))
    #-----Data handling
    #Instatiate DataSet class
    training_set = DataSet(training_data, training_class, training_index, type = 'training')
    #Put training spikes in order
    training_set.sort_spikes()
    #Use butter and savgol filter to reduce signal noise
    training_set.filter_signal()
    training_set.detect_spikes(spike_window,0.2)
    training_set.analyse_detected_peaks()

    if use_SA:
        #Begin simulated annealing process for KNN
        sa = SimulatedAnnealing(first_params,iterations,alpha,training_set.full_spikes,training_set.neuron_classes)
        best_params = sa.anneal()
        print(best_params)
    if use_grid_selection:
        #Begin grid selection for KNN
        submission_set = DataSet(submission_data, type='submission')
        submission_set.filter_signal()
        submission_set.detect_spikes(spike_window, 0.25)
        best_params = knn_grid_selection(20,5)
        print(best_params)

    if use_NN:
        #Run NN code
        nn = NeuralNetwork(len(training_set.full_spikes[0]), hidden_nodes, 5, learning_rate)
        nn.run(training_set.full_spikes, training_set.neuron_classes, training_iterations, training_proportion)

    if use_KNN:
        # Run KNN code
        knn = KNearestNeighbor(np.array(training_set.full_spikes), training_set.neuron_classes, 0.90)
        knn.create_model(4, 2)
        knn.score()
        print('Accuracy:' + f'{(knn.accuracy):.3%}')

    if create_sub:
        #Create submission dataset file
        submission_set = DataSet(submission_data, type='submission')
        submission_set.filter_signal()
        submission_set.detect_spikes(spike_window, 0.25)
        if use_NN:
            submission_classes = nn.predict(submission_set.full_spikes)
        if use_KNN:
            submission_classes = knn.predict(submission_set)
        submission_index = submission_set.neuron_index
        unique, counts = np.unique(submission_classes, return_counts=True)
        print('Submission Class counts: ')
        print(dict(zip(unique, counts)))
        class_mean = sum(counts)/len(counts)
        class_std = np.std(counts)
        print('Class mean:' + str(class_mean))
        print('Class std:' + str(class_std))
        #spio.savemat('13818.mat', mdict={'Index': np.array(submission_index), 'Class': np.array(submission_classes)})
    if show_plots:
        plt.show()
