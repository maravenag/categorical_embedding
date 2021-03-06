from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten
from keras.callbacks import EarlyStopping

class BaseModel():
    model = None
    def __init__(self, target_type=None, max_iterations=100, tolerance=5, use_hiddens=True, verbose=0):
        assert target_type in ['regression',
                               'binary_classification',
                               'multiclass'],"target_type must be 'regression' or 'binary_classification' or 'multiclass'"
        self.target_type = target_type
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.use_hiddens=use_hiddens
        self.verbose=verbose, 

    def _build_model(self, num_classes=2, vector_size=2):
        model = Sequential()
        model.add(Embedding(input_dim=num_classes,
                            output_dim=vector_size,
                            input_length=1,
                            name="embedding_layer"))
        model.add(Flatten())
        if self.use_hiddens:
            model.add(Dense(int(1.5*num_classes), activation="relu"))
            model.add(Dense(int(0.5*num_classes), activation="relu"))
        if self.target_type == "regression":
            model.add(Dense(1, activation="linear"))
            model.compile(loss='mse', optimizer='adam')
        elif self.target_type == "binary_classification":
            model.add(Dense(1, activation="sigmoid"))
            model.compile(loss='binary_crossentropy', optimizer='adam')
        else:
            model.add(Dense(num_classes, activation="softmax"))
            model.compile(loss='categorical_crossentropy', optimizer='adam')
        return model
    
    def _fit_model(self, X, y):
        stopping = EarlyStopping(monitor='loss', patience=self.tolerance)
        self.model.fit(x=X, y=y, 
                      epochs=self.max_iterations, 
                      verbose=self.verbose, 
                      callbacks=[stopping])