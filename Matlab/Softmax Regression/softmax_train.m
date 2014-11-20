%% Script for Softmax Regression
clear all; clc; close all;
A = csvread('rank_data.txt'); % reads the matrix in the csv file
y = A(:,1) + 1; % extracts the labels as a column vector
A(:,1) = 1; % sets the first column to be 1
[m, n] = size(A); % m is the number of training examples, n is the number of features


tic
k = 11; % number of possible classes
N = 10000; % number of gradient ascent steps
learn_rate = 0.0005; % learning rate for gradient ascent
C = 0.25; % parameter for Bayesian statistics

theta = TrainSoftmaxAscent(A,y,k,C,learn_rate, N);

[acc, high_conf, bad_mist, illegal] = EvaluateHypothesis(A, y, theta, 0.8)
toc