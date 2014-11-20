%% Script for Suit Cross-Validation (Softmax Regression)
clear all; clc; close all;
B = csvread('suit_data.txt'); % reads the matrix in the csv file
[m, n] = size(B); % m is the number of training examples, n is the number of features
k = 4; % number of possible classes

% Creates A_tot and y_tot, containing all the examples and labels
A_tot = B; 
y_tot = A_tot(:,1) + 1; % extracts the labels as a column vector
A_tot(:,1) = 1; % sets the first column to be 1

% Define training parameters and find theta
N_ascent = 10000; % number of gradient ascent steps
learn_rate = 0.0005; % learning rate for gradient ascent
N_newton = 15; % number of newton's method steps

% Define vector with accuracies and illegal moves
C = [0.25 0.5 1 2 4 8 16 32 64];
numC = length(C);
accuracy = zeros(numC, 1);
high_confidence = zeros(numC, 1);
bad_mistakes = zeros(numC, 1);
illegal = zeros(numC, 1);
accuracy_train = zeros(numC, 1);
high_confidence_train = zeros(numC, 1);
bad_mistakes_train = zeros(numC, 1);
illegal_train = zeros(numC, 1);

% Define CV parameters
buckets = 10;
repeat = 20; % this parameter controls how many times the program will performs the same cross-validation (on randomized sets) to average out fluctuations
mistake_limit = 0.8;
num_validate = floor(m/buckets);
num_train = m-num_validate;

for i = 1:numC % iterates over each possible value of C
    % The lines below train and test the data on the whole training set
    if (C(i) == 0)
        theta = TrainSoftmaxAscent(A_tot,y_tot,k,C(i),learn_rate,N_ascent);
    else
        theta = TrainSoftmaxNewton(A_tot,y_tot,k,C(i),learn_rate,N_newton);
    end
    [accuracy_train(i), high_confidence_train(i), bad_mistakes_train(i), illegal_train(i)] = ...
        EvaluateHypothesis(A_tot, y_tot, theta, mistake_limit, 's');
    for j = 1:repeat % iterates repeat times to average them out
        j
        A = B(randperm(m), :); % shuffles data
        y = A(:,1) + 1; % extracts the labels as a column vector
        A(:,1) = 1; % sets the first column to be 1
        for icv = 1:buckets
            icv
            % Define training and validation sets    
            validate_index = (1+num_validate*(icv-1)):(num_validate*icv);
            train_index = true(1, m);
            train_index(validate_index) = false;

            A_train = A(train_index, :);
            A_validate = A(validate_index, :);
            y_train = y(train_index);
            y_validate = y(validate_index);

            if (C(i) == 0)
                theta = TrainSoftmaxAscent(A_train,y_train,k,C(i),learn_rate,N_ascent);
            else
                theta = TrainSoftmaxNewton(A_train,y_train,k,C(i),learn_rate,N_newton);
            end

            [acc, hi_conf, bad_mist, ill] = EvaluateHypothesis(A_validate, y_validate, theta, mistake_limit, 's');

            accuracy(i) = accuracy(i) + acc;
            high_confidence(i) = high_confidence(i) + hi_conf;
            bad_mistakes(i) = bad_mistakes(i) + bad_mist;
            illegal(i) = illegal(i) + ill;    
        end
    end

    accuracy(i) = accuracy(i)/(buckets*repeat);
    high_confidence(i) = high_confidence(i)/(buckets*repeat);
    bad_mistakes(i) = bad_mistakes(i)/(buckets*repeat);
    illegal(i) = illegal(i)/(buckets*repeat);
end