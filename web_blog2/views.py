from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404



from django.contrib import messages

from django.core.mail import send_mail

from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Post, Comments, Contact

from .forms import CommentForm, ContactForm, UserInputForm, UserBook

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse

import os

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

load_dotenv()
import pandas as pd

openai.api_key = os.getenv('API_KEY')

class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-date_published']
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
             Q(title__icontains=query) | Q(body__icontains=query)
            ).distinct()

        else:
            return Post.objects.all()

def PostDetailView(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    comments = Comments.objects.filter(post=posts)  # Corrected 'posts' to 'post'
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = posts
            # new_comment.author = request.user
            new_comment.save()
            return redirect('details', pk=pk)

    return render(request, 'article_view.html', {'post': posts, 'comments': comments, 'comment_form': comment_form})


class AddBlog(CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = ['title', 'author', 'body']

    def get_success_url(self):
        return reverse_lazy('home')

class UpdatePost(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title', 'body']

    def get_success_url(self):
        return reverse_lazy('home')

def DeletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post:
        post.delete()
        deleted_post_title = post.title
        messages.success(request, f'Deleted {deleted_post_title} successfully')
        return HttpResponseRedirect(reverse('home'))
    else:

        return render(request, 'index.html', {'message': 'No post available'})

def contact_view(request):
    if request.method == 'POST':
        contact_form  = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            contact_name = contact_form.cleaned_data['name']
            contact_email = contact_form.cleaned_data['email_id']
            email_body = contact_form.cleaned_data['body']
            messages.success(request, 'We have received your feedback. Thank you.')

            from_email = 'maxbasumatry@gmail.com'
            self_recipient_list = ['maxbasumatry@gmail.com']
            self_subject = f'New Contact Form Submission - {contact_name}'
            self_message = f'Contact Name: {contact_name}\nContact Email: {contact_email}\n\n{email_body}'

            send_mail(self_subject, self_message, from_email, self_recipient_list)

            subject = 'Thank you for contacting us'
            message = f'Thank you, {contact_name}, for reaching out to us. We appreciate your feedback.'
            from_email = 'maxbasumatry@gmail.com'  # Replace with your email
            recipient_list = [contact_email]

            send_mail(subject, message, from_email, recipient_list)
            return redirect('contact')# Redirect to a success page or another appropriate view
    else:
        contact_form = ContactForm()

    return render(request, 'contact_view.html', {'contact_form': contact_form})


def contact_details(request):

    contact_details = Contact.objects.all()

    for contact in contact_details:

        print(contact.name)
        print(contact.contact_number)

    if contact_details:
        return render(request, 'contact_info.html', {'contact_details': contact_details})


# def home_view(request):
#     translation = None
#     if request.method == 'POST':
#         form = UserInputForm(request.POST)
#         if form.is_valid():
#             selected_choice = form.cleaned_data['choices']
#             language = form.cleaned_data['language']
#
#             translation = get_completion(f'translate {language} to {selected_choice}')
#             # translation = get_completion(conversation, temperature=1)
#             form = UserInputForm()
#
#
#     # return render(request, 'translator.html', {'form': form, 'translation': translation})
#
#     else:
#         form = UserInputForm()
#
#     context = {'form': form,  'translation': translation}
#
#     return render(request, 'translator.html', context)



# def get_completion(prompt, model='gpt-3.5-turbo'):
#         messages = [{"role": "user", "content": prompt}]
#         response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=0.1,  # this is the degree of randomness of the model's output
#             )
#         return response.choices[0].message["content"]


def get_completion(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

# Initialize conversation with a system message
conversation = [
        {'role': 'system', 'content': """
        You are an assistant that gives insights only about books and if asked other information. Please respond stating 'Apologies, 
        I can give only insights of Books. Greet the user everytime he says hi. In case the user has not provided the name, ask the user,
         "May I know your name?" then greet the user. Wait for the user to respond with their name. 
        After the user responds with the name, ask the user which type of book they are interested in. 
        Give them a list of options. In the first response, don't ask the user if they need further assistance.
        if user exits or says bye then respond with goodbye message.
        """}
    ]

def home_view(request):

    response = 'Welcome to my chatbot'
    default = 'Welcome to my chatbot'
    selected_choice = ''
    if request.method == 'POST':
        form = UserBook(request.POST)  # Use the correct form here
        if form.is_valid():
            selected_choice = form.cleaned_data['books']

            # Add user's message to the conversation
            conversation.append({'role': 'user', 'content': selected_choice})

            # Get response from ChatGPT based on the entire conversation
            response = get_completion(conversation, temperature=1)
            # print(f"MyBot: {response}")

            # Add ChatGPT's response to the conversation
            conversation.append({'role': 'assistant', 'content': response})

            # Print ChatGPT's response

            form = UserBook()

    else:
        form = UserBook()

    # context = {'form': form, 'response': response, 'selected_choice': selected_choice}
    # return render(request, 'translator.html', context)

    reversed_conversation = conversation[0:]

    context = {
        'form': form,
        'response': response,
        'selected_choice': selected_choice,
        'conversation': reversed_conversation,
        'default': default
    }
    return render(request, 'translator.html', context)



