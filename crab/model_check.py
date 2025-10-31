import tensorflow as tf

# Carica il modello salvato (sostituisci 'path_to_your_model.h5' con il percorso del tuo modello)
model = tf.keras.models.load_model('/eos/user/f/fsalerno/framework/MachineLearning/models/model_60_CNN_2D_new_truth_0_pt.h5')

# Ottieni l'ottimizzatore utilizzato
optimizer = model.optimizer

# Stampa il tipo dell'ottimizzatore
print("Ottimizzatore in uso:", optimizer)
print("Nome dell'ottimizzatore:", optimizer.__class__.__name__)