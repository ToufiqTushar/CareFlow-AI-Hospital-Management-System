from algorithms.model_trainer import DiseaseModelTrainer

if __name__ == "__main__":
    print("Starting ML Model Training...")
    print("=" * 50)
    
    trainer = DiseaseModelTrainer()
    accuracy = trainer.run_training()
    
    print("=" * 50)
    print(f"Training completed with accuracy: {accuracy:.2%}")
    print("Model is now ready for use in the application!")