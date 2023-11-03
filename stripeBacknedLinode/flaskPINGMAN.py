import stripe
from flask import Flask, request, redirect

app = Flask(__name__)

# Replace with your webhook secret
endpoint_secret = 'whsec_123'

# Replace with your Stripe API key
stripe.api_key = 'sk_test_51O601THRx8IgMk2MO0K3BIBPTt1Sytra8OTd8AafSz3uRCx7sOpJmuo6YtjBEiZfwPHitjeE0MfgaibTbWKASNNr00PhIDf71t'
@app.route('/ping', methods=['GET'])
def ping():
    return "success hello", 200    
@app.route('/generate_product_urls', methods=['GET'])    
def generate():
# added muy product prod_OtnlirBzHLWn4a

#TODO prodcutId
    product_id = request.args.get('productId')
    user_id = request.args.get('user_name')

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 1000,
                    "product": "prod_OtnlirBzHLWn4a",
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://172.232.194.159/success?&userId=user_1",
        cancel_url="https://example.com/error"
        # expires_at='1698620400'
    # probabilmente deve andare https
    )

    return redirect(session.url)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    payload = request.get_data()
    print(payload)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_intent = stripe.PaymentIntent.retrieve(session['payment_intent'])

        # Check if payment was successful
        if payment_intent.status == 'succeeded':
            # Grant access to user
            print ('grant_access_to_user(USER1' )

    return 'Success', 200
@app.route('/error', methods=['GET'])
def error_handler():
    print("error kokka")
    return "success", 500
@app.route('/success', methods=['GET'])
def manage_error():
    print("kokka SUCCESS")
    print (request.args.get('userId') )
    return 'success', 201

HOST='0.0.0.0'
if __name__ == '__main__':
    app.run(host=HOST,port=80,debug=True,ssl_context='adhoc')
