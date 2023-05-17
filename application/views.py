from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from myapp.models import Register
import pickle
def home(request):
    return render(request,'index.html')
def register(request):
    return render(request,'registration.html')
def about(request):
    return render(request,'about.html') 
def profile(request):
    return render(request,'profile.html') 
   
def savedata(request):
    firstname=request.POST.get("firstname")
    lastname=request.POST.get("lastname")
    city=request.POST.get("city")
    mobileno=request.POST.get("mobileno")
    emailid=request.POST.get("emailid")    
    password=request.POST.get("password")    
    obj=Register(firstname=firstname,lastname=lastname,city=city,mobileno=mobileno,emailid=emailid,password=password,)
    obj.save()
    return render(request,'index.html')
def logincheck(request):
    status=False
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        reg=Register.objects.all()
        for r in reg:
            if(r.emailid==username and r.password==password):
                status=True
                # print('here status ',status)
                break
           
        if(status==True):
            messages.success(request,"login success")
            return render(request,'main.html')
        else:
            messages.error(request,"incorrect username and password....Please try again...")
            return render(request,'index.html')




import pandas as pd
from django.shortcuts import render
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Load the one-hot encoding mapping for application and designation
with open('application\encoding_mapping.pkl', 'rb') as file:
    encoding_mapping = pickle.load(file)

import pandas as pd
from django.shortcuts import render
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Load the one-hot encoding mappings
with open('application\encoding_mapping.pkl', 'rb') as file:
    encoding_mapping = pickle.load(file)

def predictresult(request):
    if request.method == 'POST':
        # Get the input values from the user
        application = request.POST.get('a')
        designation = request.POST.get('d')
        tensile_strength = float(request.POST.get('t'))
        melting_point = float(request.POST.get('m'))

        # Load the saved model
        with open('application\model.pkl', 'rb') as file:
            clf = pickle.load(file)

        # Create a DataFrame with the input values
        input_data = pd.DataFrame([[application, designation, tensile_strength, melting_point]],
                                  columns=['Application', 'Designation', 'Tensile Strength', 'Melting Point'])

        # Apply one-hot encoding to the application and designation
        for feature, mapping in encoding_mapping.items():
            if feature in input_data.columns:
                encoded_features = pd.get_dummies(input_data[feature])
                encoded_features = encoded_features.reindex(columns=mapping, fill_value=0)
                input_data = pd.concat([input_data, encoded_features], axis=1)
                input_data.drop(feature, axis=1, inplace=True)

        # Make predictions using the loaded model
        predicted_material = clf.predict(input_data)

        # Render the result page with the predicted material
        return render(request, 'predictionresult.html', {'predicted_material': predicted_material})

    # Render the form page if it's a GET request
    return render(request, 'prediction.html')



