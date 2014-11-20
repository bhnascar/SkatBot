function [] = TestSuitFile(filename)
% TESTSUITFILE Tests the suit file for consistency
%   USAGE: TestSuitFile(filename). Filename has to be a CSV file that
%   contains the rank data as specified in the google docs. The labels must
%   come first in each row, from 0 to 3, and we must have 29 features.

    A = csvread(filename); % reads the matrix in the csv file
    [m, n] = size(A); % m is the number of training examples, n is the number of features
    y = A(:,1) + 1; % extracts the labels as a column vector (from 1 to 11)
    X = A(:,2:n); % sets X to be only features

    HowManyCardsOfEachSuit = X(:, 1:4); % this matrix contains only the features that indicate how many cards of each suit 

    % Testing for illegal moves. An illegal move is defined when, for that
    % particular training example, the features indicate that I did not have
    % the suit I chose to play.
    count_illegal = 0;
    bool_illegal = false(m,1);
    for i = 1:m
        if (HowManyCardsOfEachSuit(i, y(i)) == 0)
            count_illegal = count_illegal+1;
            bool_illegal(i) = true;
        end
    end
    disp(['We found ' int2str(count_illegal) ' illegal moves in ' int2str(m) ' training examples']);
    illegal_labels = y(bool_illegal)

    % Testing for no choice. A no-choice move is defined when, for that
    % particular training example, I only had one suit in my hand and I ended
    % up palying that suit. Note that this does not overlap with impossible or
    % illegal moves
    totalCards = sum(HowManyCardsOfEachSuit,2);
    bool_nochoice = false;
    for i = 1:m
        if (totalCards(i) == HowManyCardsOfEachSuit(i, y(i))) % if total number of cards in my hand is the same as number of cards in the suit I chose to play, then I only have one suit
            bool_nochoice(i) = true;
            i
        end
    end
    
    disp(['We found ' int2str(sum(bool_nochoice)) ' no-choice moves in ' int2str(m) ' training examples']);
    nochoice_labels = y(bool_nochoice)
end


