
# @app.route('/posts', methods=['GET', 'POST'])
# @login_required
# def posts():
#     #grab the posts from the database
    
#     posts = Posts.query.order_by(Posts.dateofbirth)

#     return render_template("posts.html", posts = posts)
# @app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_post(id):
#     post = Posts.query.get_or_404(id)
#     form = PostForm()

#     if form.validate_on_submit():
        
#         #post.author = form.author.data
#         post.age = form.age.data
#         post.gender = form.gender.data
#         post.dateofbirth = form.dateofbirth.data
#         post.firstandlast = form.firstandlast.data
#         post.laterality = form.laterality.data
#         post.date1 = form.date1.data
#         post.fovea_status = form.fovea_status.data
#         post.shadow=form.shadow.data
#         post.involved=form.involved.data
#         post.lens_status=form.lens_status.data
#         post.extent=form.extent.data
#         post.area=form.area.data
#         post.detached=form.detached.data
#         post.attached=form.attached.data
#         post.size=form.size.data
#         post.bcva=form.bcva.data
#         post.iop=form.iop.data
#         post.pvd=form.pvd.data
#         post.pvr=form.pvr.data
#         post.hemorrhage=form.hemorrhage.data
#         post.date2=form.date2.data
#         post.type=form.type.data
#         post.combined=form.combined.data
#         post.cryo=form.cryo.data
#         post.laser=form.laser.data
#         post.tech=form.tech.data
#         post.tamp=form.tamp.data
#         post.pfo=form.pfo.data
#         post.found=form.found.data
#         post.acheive=form.acheive.data
#         post.date3=form.date3.data
#         post.bcva2=form.bcva2.data
#         post.iop2=form.iop2.data
#         post.date4=form.date4.data
#         post.bcva3=form.bcva3.data
#         post.iop3=form.iop3.data
#         post.date5=form.date5.data
#         post.lens_status2=form.lens_status2.data
#         post.bcva4=form.bcva4.data
#         post.iop4=form.iop4.data
#         post.m_charth=form.m_charth.data
#         post.m_chartv=form.m_chartv.data
#         post.ask=form.ask.data
#         post.questionnaire=form.questionnaire.data
#         post.date6=form.date6.data
#         post.lens_status3=form.lens_status3.data
#         post.bcva5=form.bcva5.data
#         post.iop5=form.iop5.data
#         post.m_charth2=form.m_charth2.data
#         post.m_chartv2=form.m_chartv2.data
#         post.ask2=form.ask2.data
#         post.questionnaire2=form.questionnaire2.data
#         post.date7=form.date7.data
#         post.lens_status4=form.lens_status4.data
#         post.bcva6=form.bcva6.data
#         post.iop6=form.iop6.data
#         post.m_charth3=form.m_charth3.data
#         post.m_chartv3=form.m_chartv3.data
#         post.ask3=form.ask3.data
#         post.questionnaire3=form.questionnaire3.data

#         # Update Database
#         db.session.add(post)
#         db.session.commit()

#         # message
#         flash("Patient data has been updated!")

#         return redirect(url_for('post', id=post.id))
    
#     if current_user.id == post.poster_id:

#         #form.author.data = post.author
#         form.age.data = post.age
#         form.gender.data = post.gender
#         form.dateofbirth.data = post.dateofbirth
#         form.firstandlast.data = post.firstandlast
#         form.laterality.data = post.laterality
#         form.date1.data = post.date1
#         form.fovea_status.data = post.fovea_status
#         form.shadow.data = post.shadow
#         form.involved.data = post.involved
#         form.lens_status.data = post.lens_status
#         form.extent.data = post.extent
#         form.area.data = post.area
#         form.detached.data = post.detached
#         form.attached.data = post.attached
#         form.size.data = post.size
#         form.bcva.data = post.bcva
#         form.iop.data = post.iop
#         form.pvd.data = post.pvd
#         form.pvr.data = post.pvr
#         form.hemorrhage.data = post.hemorrhage
#         form.date2.data = post.date2
#         form.type.data = post.type
#         form.combined.data = post.combined
#         form.cryo.data = post.cryo
#         form.laser.data = post.laser
#         form.tech.data = post.tech
#         form.tamp.data = post.tamp
#         form.pfo.data = post.pfo
#         form.found.data = post.found
#         form.acheive.data = post.acheive
#         form.date3.data = post.date3
#         form.bcva2.data = post.bcva2
#         form.iop2.data = post.iop2
#         form.date4.data = post.date4
#         form.bcva3.data = post.bcva3
#         form.iop3.data = post.iop3
#         form.date5.data = post.date5
#         form.lens_status2.data = post.lens_status2
#         form.bcva4.data = post.bcva4
#         form.iop4.data = post.iop4
#         form.m_charth.data = post.m_charth
#         form.m_chartv.data = post.m_chartv
#         form.ask.data = post.ask
#         form.questionnaire.data = post.questionnaire
#         form.date6.data = post.date6
#         form.lens_status3.data = post.lens_status3
#         form.bcva5.data = post.bcva5
#         form.iop5.data = post.iop5
#         form.m_charth2.data = post.m_charth2
#         form.m_chartv2.data =  post.m_chartv2
#         form.ask2.data = post.ask2
#         form.questionnaire2.data = post.questionnaire2
#         form.date7.data = post.date7
#         form.lens_status4.data = post.lens_status4
#         form.bcva6.data = post.bcva6
#         form.iop6.data = post.iop6
#         form.m_charth3.data = post.m_charth3
#         form.m_chartv3.data =  post.m_chartv3
#         form.ask3.data = post.ask3
#         form.questionnaire3.data = post.questionnaire3


    
#         return render_template('edit_post.html', form = form)

#     else:

#         flash("You are not authorized to edit this page")

#         return render_template("index.html")

# @app.route('/dobepoct', methods=['GET', 'POST'])
# @login_required
# def dobepoct():
#     form = DobForm()
#     return render_template("dobepoct.html", form=form)
   

        
# # Patient detail stuff
# @app.route('/questionpd')
# @login_required
# def questionpd():
#     return render_template("questionpd.html")

# @app.route('/dobep', methods=['GET', 'POST'])
# @login_required
# def dobep():
#     form = DobForm()
#     user = current_user.id
#     return render_template("dobep.html", form=form, user = user)

# # Create a posts search function
# @app.route('/searched', methods=["Get","POST"])
# @login_required
# def searched():
#     form = DobForm()
#     posts = Posts.query
#     if form.validate_on_submit():
#         # get data from submitted form
#         post.dateofbirth = form.dateofbirth.data
#         post.firstandlast = form.firstandlast.data

#         #Query the database
#         posts = posts.filter(Posts.dateofbirth.like(post.dateofbirth))
#         posts = posts.filter(Posts.firstandlast.like(post.firstandlast))
#         posts = posts.order_by(Posts.firstandlast).all()
#         return render_template("searched.html", form=form, posts=posts, dateofbirth = post.dateofbirth, firstandlast = post.firstandlast)


# # Observation stuff
# @app.route('/questionod')
# @login_required
# def questionod():
#     user = current_user.id
#     return render_template("questionod.html", user=user)

# # Update Database Records
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# @login_required
# def update(id):
#     user = current_user.id

#     if user.id == 1:
#         form = UserForm()
#         name_to_update = Users.query.get_or_404(id)
#         if request.method == "POST":
#             name_to_update.name = request.form['name']
#             name_to_update.email = request.form['email']
#             name_to_update.favorite_color = request.form['favorite_color']
#             name_to_update.username = request.form['username']
#             try:
#                 db.session.commit()
#                 flash("User Updated Successfully!")
#                 return render_template("update.html", form=form, name_to_update=name_to_update, id=id, user=user)
#             except:
            
#                 flash("Error! Looks like there was a problem...try again!")
#                 return render_template("update.html", form=form, name_to_update=name_to_update, id=id, user=user)
            
#         else:
#             return render_template("update.html", form=form, name_to_update=name_to_update, id=id, user=user)


# @app.route('/delete/<int:id>')
# @login_required
# def delete(id):
#     if id == current_user.id:

#         user_to_delete = Users.query.get_or_404(id)
#         name = None
#         form = UserForm()
#         try: 
#             db.session.delete(user_to_delete)
#             db.session.commit()
#             flash("User Deleted Successfully!!")

#             our_users = Users.query.order_by(Users.date_added)
#             return render_template("add_user.html", form = form, name = name, our_users=our_users)
#         except:

#             flash("Whoops, there was a problem deleting user, try again")
#             return render_template("add_user.html", form = form, name = name, our_users=our_users)
#     else:
#             flash("You can't delete that user")

#             return redirect(url_for("dashboard"), id=id)

# Pass Stuff To Navbar
# @app.context_processor
# def base():
# 	form = SearchForm()
# 	return dict(form=form)



# # Create Search Function
# @app.route('/search', methods=["POST"])
# def search():
# 	form = SearchForm()
# 	posts = Posts.query
# 	if form.validate_on_submit():
# 		# Get data from submitted form
# 		post.searched = form.searched.data
# 		# Query the Database
# 		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
# 		posts = posts.order_by(Posts.title).all()

# 		return render_template("search.html",
# 		 form=form,
# 		 searched = post.searched,
# 		 posts = posts)


# OCT Detail stuff

# @app.route('/questionoct')
# @login_required
# def questionoct():

#     return render_template("questionoct.html")



# # Create Dashboard page
# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     form = UserForm()
#     id = current_user.id
#     name_to_update = Users.query.get_or_404(id)
#     if request.method == "POST":

#         if request.files["profile_pic"]:
#             name_to_update.profile_pic = request.files["profile_pic"]


#             pic_filename = secure_filename(name_to_update.profile_pic.filename)
            
#             pic_name = str(uuid.uuid1()) + "_" + pic_filename

#             saver = request.files['profile_pic']

#             #name_to_update.profile_pic.save(os.path.join(app.config[UPLOAD_FOLDER]), pic_name)
            
#             name_to_update.profile_pic = pic_name
#             try:
#                 db.session.commit()
#                 saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

#                 flash("User Updated Successfully!")
#                 return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
            
#             except:

#                 flash("Error! Looks like there was a problem...try again!")
#                 return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
#         else:
#             db.session.commit()
#             flash("User Updated Successfully!")
#             return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
        
#     else:    


#         return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)


# @app.route('/dobnpoct', methods=['GET', 'POST'])
# @login_required
# def dobnpoct():
#     user = current_user.id
#     form = IDForm()

#     if form.validate_on_submit():
#         poster = current_user.id
#         post = Posts(poster_id = poster, dateofbirth=form.dateofbirth.data, firstandlast=form.firstandlast.data)
#         form.dateofbirth.data = ''
#         form.firstandlast.data = ''

#         # add post data to the database

#         db.session.add(post)
#         db.session.commit()
#         #return a message
#         flash("Profile Created Successfully!")


#     return render_template("dobnpoct.html", form=form, user = user)


# # POSTS STUFF
# @app.route('/posts/<int:id>')
# @login_required
# def post(id):
#     post = Posts.query.get_or_404(id)
#     return render_template('post.html', post = post)
  
        #   <!-- <li class="nav-item">
        #     <a class="nav-link" href="{{ url_for('add_user') }}">Register</a>
        #   </li> -->