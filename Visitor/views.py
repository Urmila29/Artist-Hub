from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate 
from .models import *
from Admin.models import *
from Artist.models import *
from django.core.mail import send_mail
from django.conf import settings
from random import *
import datetime
import razorpay
# ---------------------------- U S E R   A C C E S S ---------------------------- #
def UserAccessPage(request):
    if 'id' in request.session and 'emailaddress' in request.session:
        user = AAdmin.objects.get(id=request.session['id'])
        if user.Role == 'Artist':
            artist = AArtist.objects.get(admin=user)
            return artist
        elif user.Role == 'Visitor':
            visitor = VVisitor.objects.get(admin=user)
            return visitor
# ----------------------------- I N D E X   P A G E ----------------------------- #
def IndexPage(request):
    user = UserAccessPage(request)
    if user:
        return render(request, "Visitor/index.html", {'user': user})
    else:
        return render(request, "Visitor/index.html")
# -------------------------- R E G I S T E R   P A G E -------------------------- #
def RegisterPage(request):
    return render(request, "Visitor/register.html")
# -------------------------- R E G I S T E R   U S E R -------------------------- #
def RegisterUserPage(request):
    if request.method == 'POST':
        role = request.POST['role']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['emailaddr']
        pwd = request.POST['password']
        rpwd = request.POST['password-repeat']
        nation = request.POST['country']
        mobno = request.POST['mobileno']
        bdate = request.POST['bdate']
        currentaddr = request.POST['currentaddr']
        permanentaddr = request.POST['permanentaddr']
        gender = request.POST['gender']
        profile = request.FILES['profile']

        user = AAdmin.objects.filter(Email=email)

        if len(user) > 0:
            msg = f"{email} already exists."
            return render(request, "Visitor/login.html", {'errmsg': msg})
        else:
            valid_password = (pwd == rpwd)
            if valid_password == False:
                msg = "Password does not match."
                return render(request, "Visitor/register.html", {'errmsg': msg})
            else:
                user = AAdmin.objects.create(Email=email, Role=role, Password=pwd)
                if role == 'Artist':
                    artist = AArtist.objects.create(admin=user, Firstname=fname, Lastname=lname, Nationality=nation, Mobileno=mobno, Birthdate=bdate, Currentaddr=currentaddr, Permanentaddr=permanentaddr, Gender=gender, ProfilePic=profile)
                elif role == 'Visitor':
                    visitor = VVisitor.objects.create(admin=user, Firstname=fname, Lastname=lname, Nationality=nation, Mobileno=mobno, Birthdate=bdate, Currentaddr=currentaddr, Permanentaddr=permanentaddr, Gender=gender, ProfilePic=profile)
                msg = "You have registered successfully...!"
                return render(request, "Visitor/login.html", {'msg': msg})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/register.html", {'errmsg': msg})
# ----------------------------- L O G I N   P A G E ----------------------------- #
def LoginPage(request):
    return render(request, "Visitor/login.html")
# ----------------------------- L O G I N   U S E R ----------------------------- #
def LoginUserPage(request):
    if request.method == 'POST':
        email = request.POST['emailaddress']
        password = request.POST['pwd']
        role = request.POST['role']
        if role == 'Admin':
            user = authenticate(username=email, password=password)
            if user: 
                request.session['role'] = 'Admin'
                msg = "Welcome Admin"
                return render(request, "Visitor/index.html", {'msg': msg})
            else:
                msg = "This admin is not found."
                return render(request, "Visitor/index.html", {'errmsg': msg})
        elif role == "Artist" or role == "Visitor":
            user = AAdmin.objects.filter(Email=email)
            if len(user) == 1:
                if user[0].Password == password:
                    request.session['id'] = user[0].id
                    request.session['emailaddress'] = user[0].Email
                    request.session['role'] = user[0].Role
                    return redirect('/')
                else:
                    msg = "Password does not match."
                    return render(request, "Visitor/login.html", {'errmsg': msg})
            else:
                msg = f"{email} does not exist."
                return render(request, "Visitor/login.html", {'errmsg': msg})

    else:
        msg = "Request changed to get."
        return render(request, "Visitor/login.html", {'errmsg': msg})
# ---------------------------- L O G O U T   U S E R ---------------------------- #
def LogOutPage(request):
    if request.session['role'] == 'Admin':
        del request.session['role']
        logout(request)
        return render(request, "Visitor/index.html")
    else:
        del request.session['id']
        del request.session['emailaddress']
        del request.session['role']
        return render(request, "Visitor/index.html")
# ------------------------ F O R G O T   P A S S W O R D ------------------------ #
def ForgotPasswordPage(request):
    return render(request, "Visitor/emailverification.html")
# -------------------------- E - M A I L   V E R I F Y -------------------------- #
def EmailVerificationPage(request):
    if request.method == 'POST':
        email = request.POST['emailaddress']

        user = AAdmin.objects.filter(Email=email)

        if len(user) > 0:
            euser = AAdmin.objects.get(Email=email)
            return render(request, "Visitor/otpverification.html", {'admin': euser})
        else:
            msg = "Please type your correct E-mail address."
            return render(request, "Visitor/emailverification.html", {'errmsg': msg})
# ----------------------- O T P   V E R I F I C A T I O N ----------------------- #
def OTPVerificationPage(request):
    if request.method == 'POST':
        email = request.POST['emailaddress']
        user = AAdmin.objects.filter(Email=email)

        if len(user) > 0:
            euser = AAdmin.objects.get(Email=email)
            subject = "Forgot your Password...??"
            otp = ""
            for i in range(6):
                otp += str(randint(0, 9))
            euser.OTP = otp
            euser.save()
            msg = f"Your OTP is {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, msg, email_from, recipient_list)
            return render(request, "Visitor/changepassword.html", {'admin': euser})
        else:
            msg = "Oops... Please enter correct OTP...!"
            return render(request, "Visitor/emailverification.html", {'errmsg': msg})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/otpverification.html", {'errmsg': msg})
# ----------------------- O T P   V E R I F I C A T I O N ----------------------- #
def PasswordChangingPage(request):
    if request.method == 'POST':
        email = request.POST['emailaddress']
        password = request.POST['password']
        repeatpassword = request.POST['repeat-password']

        user = AAdmin.objects.get(Email=email)

        if password == repeatpassword:
            user.Password = password
            user.save()
            msg = "Your password is changed successfully."
            d = {'admin': user, 'msg': msg}
            return render(request, "Visitor/login.html", d)
        else:
            msg = "Passwords are not matched."
            return render(request, "Visitor/changepassword.html", {'errmsg': msg})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/changepassword.html", {'errmsg': msg})
# --------------------------- U S E R   P R O F I L E --------------------------- #
def UserProfilePage(request):
    user = UserAccessPage(request)
    return render(request, "Visitor/myaccount.html", {'user': user})
# ------------------------- U P D A T E   P R O F I L E ------------------------- #
def UpdateProfilePage(request, pk):
    user = UserAccessPage(request)
    if request.method == 'POST':
        adminid = AAdmin.objects.get(id=pk)
        if adminid.Role == 'Artist':
            user = AArtist.objects.get(admin=adminid)
            user.Firstname = request.POST['firstname'] if request.POST['firstname'] else user.Firstname
            user.Lastname = request.POST['lastname'] if request.POST['lastname'] else user.Lastname
            user.Profession = request.POST['profession'] if request.POST['profession'] else user.Profession
            adminid.Email = request.POST['email'] if request.POST['email'] else adminid.Email
            user.Mobileno = request.POST['mobileno'] if request.POST['mobileno'] else user.Mobileno
            user.Birthdate = request.POST['bdate'] if request.POST['bdate'] else user.Birthdate
            user.Currentaddr = request.POST['caddr'] if request.POST['caddr'] else user.Currentaddr
            user.Permanentaddr = request.POST['paddr'] if request.POST['paddr'] else user.Permanentaddr
            user.Gender = request.POST['gender'] if request.POST['gender'] else user.Gender
            user.Nationality = request.POST['country'] if request.POST['country'] else user.Nationality
            user.Myself = request.POST['myself'] if request.POST['myself'] else user.Myself
            user.ProfilePic = request.POST['profile'] if request.POST['profile'] else user.ProfilePic
            cpwd = request.POST['current-password']
            if cpwd:
                if cpwd == adminid.Password:
                    npwd = request.POST['new-password']
                    rpwd = request.POST['repeat-password']
                    if npwd == rpwd:
                        adminid.Password = npwd
                        msg = "New password generated successfully..!"
                        d = {'user': user, 'msg': msg}
                        user.save()
                        adminid.save()
                        return render(request, "Visitor/updateprofile.html", d)
                    else:
                        msg = "Oops... Passwords are not matched..!!"
                        d = {'user': user, 'msg': msg}
                        user.save()
                        adminid.save()
                        return render(request, "Visitor/updateprofile.html", d)
                else:
                    msg = "Current password is wrong."
                    user.save()
                    adminid.save()
                    d = {'user': user, 'msg': msg}
                    return render(request, "Visitor/updateprofile.html", d)
            msg = "Updated Succesfully..!!"
            user.save()
            adminid.save()
            d = {'user': user, 'msg': msg}
            return render(request, "Visitor/updateprofile.html", d)
        if adminid.Role == 'Visitor':
            user = VVisitor.objects.get(admin=adminid)
            user.Firstname = request.POST['firstname'] if request.POST['firstname'] else user.Firstname
            user.Lastname = request.POST['lastname'] if request.POST['lastname'] else user.Lastname
            adminid.Email = request.POST['email'] if request.POST['email'] else adminid.Email
            user.Mobileno = request.POST['mobileno'] if request.POST['mobileno'] else user.Mobileno
            user.Birthdate = request.POST['bdate'] if request.POST['bdate'] else user.Birthdate
            user.Currentaddr = request.POST['caddr'] if request.POST['caddr'] else user.Currentaddr
            user.Permanentaddr = request.POST['paddr'] if request.POST['paddr'] else user.Permanentaddr
            user.Gender = request.POST['gender'] if request.POST['gender'] else user.Gender
            user.Nationality = request.POST['country'] if request.POST['country'] else user.Nationality
            user.Myself = request.POST['myself'] if request.POST['myself'] else user.Myself
            user.ProfilePic = request.POST['profile'] if request.POST['profile'] else user.ProfilePic
            cpwd = request.POST['current-password']
            if cpwd:
                if cpwd == adminid.Password:
                    npwd = request.POST['new-password']
                    rpwd = request.POST['repeat-password']
                    if npwd == rpwd:
                        adminid.Password = npwd
                        msg = "New password generated successfully..!"
                        d = {'user': user, 'msg': msg}
                        user.save()
                        adminid.save()
                        return render(request, "Visitor/updateprofile.html", d)
                    else:
                        msg = "Oops... Passwords are not matched..!!"
                        d = {'user': user, 'msg': msg}
                        user.save()
                        adminid.save()
                        return render(request, "Visitor/updateprofile.html", d)
                else:
                    msg = "Current password is wrong."
                    user.save()
                    adminid.save()
                    d = {'user': user, 'msg': msg}
                    return render(request, "Visitor/updateprofile.html", d)
            msg = "Updated Succesfully..!!"
            user.save()
            adminid.save()
            d = {'user': user, 'msg': msg}
            return render(request, "Visitor/updateprofile.html", d)
    else:
        return render(request, "Visitor/updateprofile.html", {'user': user})
# --------------------------- F I N D   A R T I S T S --------------------------- #
def FindArtist(request):
    user = UserAccessPage(request)
    return render(request, "Visitor/findartist.html", {'user': user})
# --------------------------- F I N D   A R T I S T S --------------------------- #
def FindArtistsPage(request):
    if request.method == 'POST':
        choice = request.POST['choice']
        user = UserAccessPage(request)
        if choice == "Name":
            letter = request.POST['letter']
            artists = AArtist.objects.filter(Firstname__startswith=letter)
            if artists:
                return render(request, "Visitor/findartist.html", {'artists': artists}, {'user': user})
            else:
                msg = "Artist not found."
                return render(request, "Visitor/findartist.html", {'errmsg': msg}, {'user': user})
        elif choice == "Location":
            place = request.POST['placename']
            artists = AArtist.objects.filter(Nationality=place)
            if artists:
                return render(request, "Visitor/findartist.html", {'artists': artists}, {'user': user})
            else:
                msg = "Artist not found."
                return render(request, "Visitor/findartist.html", {'errmsg': msg}, {'user': user})
        elif choice == "Profession":
            profession = request.POST['profession']
            artists = AArtist.objects.filter(Profession=profession)
            if artists:
                return render(request, "Visitor/findartist.html", {'artists': artists}, {'user': user})
            else:
                msg = "Artist not found."
                return render(request, "Visitor/findartist.html", {'errmsg': msg}, {'user': user})
        else:
            artists = AArtist.objects.all()
            return render(request, "Visitor/findartist.html", {'artists': artists}, {'user': user})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/findartist.html")
# ---------------------------- B O O K   A R T I S T ---------------------------- #
def BookArtistPage(request, pk):
    bookartist = AArtist.objects.get(id=pk)
    user = UserAccessPage(request)
    return render(request, "Visitor/bookartist.html", {'artist': bookartist, 'user': user})
# --------------------------- B O O K   R E Q U E S T --------------------------- #
def BookArtistRequestsPage(request, pk):
    if request.method == 'POST':
        user = UserAccessPage(request)
        eventname = request.POST['event']
        location = request.POST['place']
        eventdate = request.POST['date']
        minbudget = request.POST['minbudget']
        maxbudget = request.POST['maxbudget']
        description = request.POST['description']
        visitorid = AAdmin.objects.get(id=request.session['id'])
        visitoruser = VVisitor.objects.get(admin=visitorid)
        artistid = AArtist.objects.get(id=pk)
        bookedrequest = BookingRequests.objects.create(artist=artistid, visitor=visitoruser, Event=eventname, Place=location, Event_Date=eventdate, Minimum_Budget=minbudget, Maximum_Budget=maxbudget, Description=description)
        msg = "Your request submitted successfully."
        return render(request, "Visitor/requests.html", {'msg': msg}, {'user': user})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/bookartist.html", {'errmsg': msg})
# -------------------------- R E Q U E S T S   P A G E -------------------------- #
def RequestsPage(request):
    user = UserAccessPage(request)
    return render(request, "Visitor/requests.html", {'user': user})
# -------------------- S H O W   R E Q U E S T S   P A G E ---------------------- #
def ShowRequestsPage(request, pk):
    if request.method == 'POST':
        choice = request.POST['choice']
        user = AAdmin.objects.get(id=request.session['id'])
        if user.Role == 'Artist':
            artistreq = AArtist.objects.get(admin=user)
            if choice == "Pending" or choice == "Cancelled" or choice == "Approved":
                pendingrequests = BookingRequests.objects.filter(Status=choice, artist=artistreq)
                return render(request, "Visitor/requests.html", {'requests': pendingrequests, 'user': user})
            else:
                allrequests = BookingRequests.objects.filter(artist=artistreq)
                return render(request, "Visitor/requests.html", {'requests': allrequests, 'user': user})
        elif user.Role == "Visitor":
            if choice == "Pending" or choice == "Cancelled" or choice == "Approved":
                visitorreq = VVisitor.objects.get(admin=user)
                requests = BookingRequests.objects.filter(Status=choice, visitor=visitorreq)
                return render(request, "Visitor/requests.html", {'requests': requests, 'user': user})
            else:
                allrequests = BookingRequests.objects.filter(visitor_id=pk)
                return render(request, "Visitor/requests.html", {'requests': allrequests, 'user': user})
    else:
        msg="Request changed to get."
        return render(request, "Visitor/requests.html", {'errmsg': msg})
# ------------------------- R E Q U E S T   S T A T U S ------------------------- #
def UpdateRequestsPage(request, pk):
    if request.method == 'POST':
        resstatus = request.POST['status']
        reqstatus = BookingRequests.objects.get(id=pk)
        reqstatus.Status = resstatus
        reqstatus.save()
        user = UserAccessPage(request)
        msg = "Request status changed successfully."
        return render(request, "Visitor/requests.html", {'user': user, 'msg': msg})
# ------------------------- P A Y M E N T   S T A T U S ------------------------- #
def PaymentProcessPage(request, pk):
    if request.method == "POST":
        user = BookingRequests.objects.get(id=pk)
        return render(request, 'Visitor/paymentprocess.html', {'user': user})
    else:
        msg="Request changed to get."
        return render(request, "Visitor/paymentprocess.html", {'errmsg': msg})
# ------------------------ P A Y M E N T   S U C C E S S ------------------------ #
def PaymentSuccessPage(request, pk):
    if request.method == "POST":
        name = request.POST.get['name']
        amount = int(name) * 100
        request.session['amt'] = amount
        client = razorpay.Client(
            auth=("rzp_test_Y7pvAH8A4RYcZm", "xUaVVQofPXzb8KsEXufO9V9Z"))
        payme = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
        bookedartist = AArtist.objects.get(id=pk)
        return render(request, 'HR_app/paymentsuccessfull.html', {'user': bookedartist})
    else:
        msg="Request changed to get."
        return render(request, "Visitor/paymentprocess.html", {'errmsg': msg})
# ------------------------------ D A S H B O A R D ------------------------------ #
def DashboardPage(request):
    user = UserAccessPage(request)
    return render(request, "Visitor/dashboard.html", {'user': user})
# ------------------------- D E L E T E   A C C O U N T ------------------------- #
def DeleteAccountPage(request, pk):
    if request.session['role'] == 'Admin':
        user = AAdmin.objects.get(id=pk)
        user.delete()
        if user.Role == "Artist":
            return AllArtistPage(request)
        else:
            return AllVisitorPage(request)
    else:
        user = UserAccessPage(request)
        adminuser = AAdmin.objects.get(id=request.session['id'])
        user.delete()
        adminuser.delete()
        LogOutPage(request)
        msg = "Your account has been deleted successfully."
        return render(request, "Visitor/index.html", {'msg': msg})
# -------------------------------- R E V I E W S -------------------------------- #
def GiveReviewsPage(request, pk):
    user = UserAccessPage(request)
    reviewArtist = BookingRequests.objects.filter(visitor_id=pk)
    if reviewArtist:
        return render(request, "Visitor/reviews.html", {'reviewartist': reviewArtist, 'user': user})
    else:
        msg = "You haven't booked any Artist."
        return render(request, "Visitor/reviews.html", {'errmsg': msg,'user': user})
# ------------------------- S U B M I T   R E V I E W S ------------------------- #
def EnterReviews(request, pk):
    if request.method == 'POST':
        user = UserAccessPage(request)
        reviewartist = BookingRequests.objects.get(id=pk)
        return render(request, "Visitor/submitreview.html", {'user': user, 'reviewartist': reviewartist})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/submitreview.html")
# ---------------------------- A L L   R E V I E W S ---------------------------- #
def AllReviews(request, pk):
    user = UserAccessPage(request)
    adminuser = AAdmin.objects.get(id=request.session['id'])
    if adminuser.Role == 'Artist':
        allreview = Reviews.objects.filter(artist_id=pk)
        if allreview:
            return render(request, "Visitor/reviewsall.html", {'all': allreview, 'user': user})
        else:
            msg = "You haven't got any review."
            return render(request, "Visitor/reviewsall.html", {'user': user, 'errmsg': msg})
    elif adminuser.Role == 'Visitor':
        allReview = Reviews.objects.filter(visitor_id=pk)
        if allReview:
            return render(request, "Visitor/reviewsall.html", {'all': allReview, 'user': user})
        else:
            msg = "You haven't submitted any review."
            return render(request, "Visitor/reviewsall.html", {'user': user, 'errmsg': msg})
# ------------------------- S U B M I T   R E V I E W S ------------------------- #
def SubmitReviews(request, pk):
    if request.method == 'POST':
        on_budget = request.POST['radio']
        on_time = request.POST['radio2']
        rate = request.POST['rating']
        message = request.POST['message2']
        visitorid = UserAccessPage(request)
        artistid = AArtist.objects.get(id=pk)
        bookedrequest = Reviews.objects.create(artist=artistid, visitor=visitorid, On_Budget=on_budget, On_Time=on_time, Rate=rate, Review=message)
        return AllReviews(request, pk)
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/reviewsall.html")    
# ----------------------- S H O W   E D I T   R E V I E W S --------------------- #
def ShowSubmittedReview(request, pk):
    user = UserAccessPage(request)
    sreview = Reviews.objects.get(id=pk)
    return render(request, "Visitor/submittedreview.html", {'user': user, 'review': sreview})
# ---------------------------- E D I T   R E V I E W S -------------------------- #
def EditReviews(request, pk):
    if request.method == 'POST':
        user = UserAccessPage(request)
        review = Reviews.objects.get(id=pk)
        review.On_Budget = request.POST['radio'] if request.POST['radio'] else review.On_Budget
        review.On_Time = request.POST['radio2'] if request.POST['radio2'] else review.On_Time
        review.Rate = request.POST['rating'] if request.POST['rating'] else review.Rate
        review.Review = request.POST['message2'] if request.POST['message2'] else review.Review
        review.save()
        msg = "Your review is editted successfully."
        return render(request, "Visitor/reviewsall.html", {'user': user, 'msg': msg})
    else:
        msg = "Request change to get."
        return render(request, "Visitor/reviewsall.html", {'msg': msg})        
# ------------------- F E E D B A C K   &   C O M P L A I N T ------------------- #
def FeedbackAndComplaints(request):
    user = UserAccessPage(request)
    return render(request, "Visitor/feedbackcomplaint.html", {'user': user})
# ------------ S U B M I T   F E E D B A C K   &   C O M P L A I N T ------------ #
def SubmitFeedbackAndComplaints(request):
    if request.method == 'POST':
        name = request.POST['name']
        mail = request.POST['email']
        sub = request.POST['subject']
        msg = request.POST['comments']
        user = UserAccessPage(request)
        feedback = FeedbackOrComplaints.objects.create(User_Name=name, Email=mail, Subject=sub, Message=msg)
        msg = "Thank you for your opinion...!!"
        return render(request, "Visitor/feedbackcomplaint.html", {'user': user, 'msg': msg})
    else:
        msg = "Request changed to get."
        return render(request, "Visitor/feedbackcomplaint.html", {'errmsg': msg})
# ---------------------------- A L L   A R T I S T S ---------------------------- #
def AllArtistPage(request):
    alla = AArtist.objects.all()
    return render(request, "Visitor/dashboard.html", {'all': alla, 'msg': 'All Artists'})
# --------------------------- A L L   V I S I T O R S --------------------------- #
def AllVisitorPage(request):
    allv = VVisitor.objects.all()
    return render(request, "Visitor/dashboard.html", {'all': allv, 'msg': 'All Visitors'})
# -------------- A L L   F E E D B A C K   &   C O M P L A I N T S -------------- #
def AllFeedbackAndComplaints(request):
    allfc = FeedbackOrComplaints.objects.all()
    print("===============================", allfc)
    return render(request, "Visitor/dashboard.html", {'fc': allfc, 'msg': 'All feedbacks & Complaints'})