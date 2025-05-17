from tfshutupper import shutup; shutup()
from main import main

def batcher(CSV_FILE_PATH):
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
		predicts.append(main(CSV_FILE_PATH))

	print()
	print("-------------------------------------------")
	print()

	for item in predicts:
		print(f"Predicted price: ${item:.2f}")


	print(f"Average predicted price: ${sum(predicts)/len(predicts)}")
	return sum(predicts)/len(predicts)

if __name__ == "__main__":
	batcher("historicaldata/HDnvda5y.csv")