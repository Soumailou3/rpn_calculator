from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

stack = []

class CalculatorStack(Resource):
    def get(self):
        """
        Récupère l'état actuel de la pile
        ---
        responses:
          200:
            description: État actuel de la pile
        """
        return jsonify({'stack': stack})
    
    def post(self):
        """
        Ajoute un nombre à la pile
        ---
        parameters:
          - name: number
            in: body
            required: true
            schema:
              type: object
              properties:
                value:
                  type: number
        responses:
          201:
            description: Nombre ajouté avec succès
        """
        data = request.get_json()
        number = data.get('value')
        if number is not None:
            stack.append(float(number))
            return {'message': 'Number added successfully'}, 201
        return {'error': 'Invalid input'}, 400

class CalculatorOperation(Resource):
    def post(self, operation):
        """
        Effectue une opération sur les deux derniers nombres de la pile
        ---
        parameters:
          - name: operation
            in: path
            type: string
            enum: ['+', '-', '*', '/']
            required: true
        responses:
          200:
            description: Opération effectuée avec succès
        """
        if len(stack) < 2:
            return {'error': 'Not enough operands'}, 400

        b = stack.pop()
        a = stack.pop()

        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/':
            if b == 0:
                stack.append(a)
                stack.append(b)
                return {'error': 'Division by zero'}, 400
            result = a / b
        else:
            stack.append(a)
            stack.append(b)
            return {'error': 'Invalid operation'}, 400

        stack.append(result)
        return {'result': result}

class CalculatorClear(Resource):
    def post(self):
        """
        Nettoie la pile
        ---
        responses:
          200:
            description: Pile nettoyée avec succès
        """
        stack.clear()
        return {'message': 'Stack cleared'}

api.add_resource(CalculatorStack, '/stack')
api.add_resource(CalculatorOperation, '/operate/<string:operation>')
api.add_resource(CalculatorClear, '/clear')

if __name__ == '__main__':
    app.run(debug=True)