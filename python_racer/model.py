import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os # to save model

#now we want to implement 2 classes: 1 for the model & one for the trainer
class Linear_Qnet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self,x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, filename = 'model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), filename)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self,state, action, reward, next_state, done): 
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x) -->if it has multiple vals

        #to handle multi sizes
        if len(state.shape) == 1:
            #(1,x) 
            state = torch.unsqueeze(state,0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )


        #predicted Q values with the current state
        pred  = self.model(state) #pred -->action

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

        #Set target of maximum value action
        target[idx][torch.argmax(action).item()] = Q_new


        # Q_new = reward + gamma * max(next predicted) Q value
        #pred.clone()
        #preds[argmax(action)] = Q_new

        # eg of action-->[1 ,0, 0] -->here, the 1 is set to the new Q value

        self.optimizer.zero_grad()
        #calc loss
        self.criterion(target, pred)
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()