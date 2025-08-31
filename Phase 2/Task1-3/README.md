# **Report**

## **Adversarial Attack Documentation**

### **Fast Gradient Sign Method (FGSM):**
It is a white-box attack, meaning it requires knowledge of the model’s architecture and parameters. The idea is to perturb the input data by adding a small amount of noise based on the gradient of the loss with respect to the input. The simplicity of FGSM lies in its effectiveness in creating adversarial examples with minimal computational cost.

**Equation:** $\nabla_x J(\theta, x, y) = \frac{\partial x}{\partial J}$

#### **Advantages of FGSM**
1) Simplicity
2) Efficiency
3) Transferability

#### **Limitations**
1) Limited Robustness
2) Known Vulnerability

#### **Code**
```bash
def fgsm_attack(model, images, labels, epsilon, loss_fn):
    images = images.clone().detach().to(device)
    labels = labels.clone().detach().to(device)
    images.requires_grad = True

    outputs = model(images)
    loss = loss_fn(outputs, labels)
    model.zero_grad()
    loss.backward()

    data_grad = images.grad.data
    perturbed_images = images + epsilon * data_grad.sign()
    perturbed_images = torch.clamp(perturbed_images, 0, 1)

    noise = perturbed_images - images
    return perturbed_images.detach(), noise.detach()
```

#### **Evaluation ASR (Attack Success Rate)**
```bash
def evaluate_under_attack(model, loader, epsilons, loss_fn, max_batches=None):
    model.eval()
    acc, asr = {}, {}
    
    clean_preds = []
    clean_labels = []
    for b, (x, y) in enumerate(loader):
        if max_batches is not None and b >= max_batches: break
        x, y = x.to(device), y.to(device)
        with torch.no_grad():
            logits = model(x)
            clean_preds.append(logits.argmax(1))
            clean_labels.append(y.clone())
    clean_preds = torch.cat(clean_preds, dim=0)
    clean_labels = torch.cat(clean_labels, dim=0)

    for eps in epsilons:
        total_correct = 0
        total = 0
        total_success = 0
        offset = 0
        for b, (x, y) in enumerate(loader):
            if max_batches is not None and b >= max_batches: break
            x, y = x.to(device), y.to(device)
            x_adv, _ = fgsm_attack(model, x, y, eps, loss_fn)
            logits_adv = model(x_adv)
            pred_adv = logits_adv.argmax(1)

            # Accuracy under attack
            total_correct += (pred_adv == y).sum().item()
            total += y.numel()

            # ASR relative to clean predictions for this slice
            k = y.size(0)
            pred_clean_slice = clean_preds[offset:offset+k]
            total_success += (pred_adv != pred_clean_slice.to(device)).sum().item()
            offset += k

        acc[eps] = 100.0 * total_correct / total
        asr[eps] = 100.0 * total_success / total
        print(f"Epsilon={eps:.4f} | Adv Acc: {acc[eps]:.2f}% | ASR: {asr[eps]:.2f}%")
```
---
## **Defense Documentation**

### **Adversarial Training:**
The most direct and basic 
defense. Modify your training loop to generate 
adversarial examples for each batch and train the 
model to correctly classify both the clean and 
attacked images. This teaches the model to 
recognize its own weaknesses. 

#### **Results**
1) **Model of Phase1**

    - Test Accuracy: 89.94% | Test Loss: 0.4328

    - Epsilon=0.3000 | Adv Acc: 23.73% | ASR: 79.49%

2) **Hardened Model**
    - Test Accuracy: 90.48% | Test Loss: 0.4098

    - Epsilon=0.3000 | Adv Acc: 59.14% | ASR: 36.18%
---
## **Resources I used**
[Link1](https://medium.com/@yoshisauce/understanding-fgsm-a-more-intuitive-approach-to-adversarial-attacks-0e4d59f2f268)

[Link2](https://medium.com/@zachariaharungeorge/a-deep-dive-into-the-fast-gradient-sign-method-611826e34865)

[Link3](https://medium.com/@kemalpiro/xai-methods-saliency-ef3841eae910)

[Link4](https://medium.com/@kdk199604/grad-cam-a-gradient-based-approach-to-explainability-in-deep-learning-871b3ab8a6ce)