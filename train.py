from nltk_utils import tokenize, stem, bag_of_words
from model import NeuralNet


import json
import numpy as np


import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

with open("intents.json", "r") as file:
    intents = json.load(file)

tags = []
all_words = []
xy = []

for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        tokenized_pattern = tokenize(pattern)
        all_words.extend(tokenized_pattern)
        xy.append((tokenized_pattern, tag))
ignore_words = ["!", "?", ".", ","]

all_words = [stem(word) for word in all_words if word not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

x_train = []
y_train = []

for (tokenized_sentence, tag )in xy:
    bag = bag_of_words(tokenized_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    #dataset[index]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples
    
#hyperparams
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(bag)
learning_rate = 0.001
num_epochs = 1000



dataset = ChatDataset()
train_loader = DataLoader(dataset, batch_size, shuffle=True, num_workers=2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuralNet(input_size, hidden_size, output_size).to(device)

#loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels  = labels.to(device)

        #forward
        outputs = model(words)
        loss = criterion(outputs, labels)

        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    #print every 100 steps
    if (epoch +1) % 100 == 0:
        print(f"epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}")

print(f"final loss, loss={loss.item():.4f}")

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f"training complete. file saved to {FILE}")