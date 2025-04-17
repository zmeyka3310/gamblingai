from tfshutupper import shutup; shutup()
from main import main

batches = 10
predicts = []

for i in range(batches):
	print("-------------------------------------------")
	print("")
	print("")
	print(f"Doing batch {i+1}/{batches}")
	print("")
	print("")
	print("-------------------------------------------")
	predicts.append(main())

print()
print("-------------------------------------------")
print()

for item in predicts:
	print(f"Predicted price: ${item:.2f}")


print(f"Average predicted price: ${sum(predicts)/len(predicts)}")