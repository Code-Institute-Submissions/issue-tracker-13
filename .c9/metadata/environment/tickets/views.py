{"filter":false,"title":"views.py","tooltip":"/tickets/views.py","undoManager":{"mark":7,"position":7,"stack":[[{"start":{"row":12,"column":18},"end":{"row":12,"column":60},"action":"remove","lines":["sk_test_4m8kvv7vxb5ggTkQO0cXkgkK00d9dxL5up"],"id":814},{"start":{"row":12,"column":18},"end":{"row":12,"column":60},"action":"insert","lines":["sk_test_4m8kvv7vxb5ggTkQO0cXkgkK00d9dxL5up"]}],[{"start":{"row":0,"column":0},"end":{"row":205,"column":45},"action":"remove","lines":["from django.shortcuts import render, reverse, redirect, get_object_or_404","from django.contrib.auth.decorators import login_required","from django.core.mail import EmailMessage","from django.contrib import messages","from django.utils import timezone","from django.conf import settings","from .models import Ticket","from .forms import TicketForm, PaymentForm","from comments.models import Comment","from comments.forms import CommentForm","import stripe","","stripe.api_key = \"sk_test_4m8kvv7vxb5ggTkQO0cXkgkK00d9dxL5up\"","","# Create your views here.","def all_tickets(request, sort=None):","    if sort == 'bugs':","        tickets = Ticket.objects.filter(ticket_type='Bug')","    elif sort =='feature_requests':","        tickets = Ticket.objects.filter(ticket_type='Feature Request')","    else:","        tickets = Ticket.objects.all()","    return render(request, 'index.html', {'tickets': tickets})","    ","","@login_required    ","def upvote(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    ticket.upvotes += 1","    ticket.save()","    messages.error(request, \"Upvote recorded!\")","    return redirect(ticket_detail, ticket.pk)","    ","@login_required","def upvote_payment(request, pk):","    ","    ticket = get_object_or_404(Ticket, pk=pk)","    ","    if request.method==\"POST\":","        payment_form = PaymentForm(request.POST)","        if payment_form.is_valid():","            try:","                customer = stripe.Charge.create(amount = 500,","                                                currency = \"eur\",","                                                description = request.user.email,","                                                card = payment_form.cleaned_data['stripe_id'],","                                                )","            except:","                messages.error(request, \"Your card was declined\")","                ","            if customer.paid:","                messages.error(request, \"Your payment was successful\")","                new_total = float(ticket.total_paid) + (customer.amount/100)","                ticket.total_paid = new_total","                ticket.save()","                return redirect(upvote, ticket.id)","                ","            else:","                messages.error(request, \"Unable to take payment\")","        ","        else:","            print(payment_form.errors)","            messages.error(request, \"We were unable to take payment with that card\")","            ","    else:","        payment_form = PaymentForm()","        ","    return render(request, \"upvote-payment.html\", {'ticket': ticket, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})","                ","    ","def ticket_detail(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    comments = Comment.objects.filter(comment='user')","    ","    if request.method == \"POST\":","        comment_form = CommentForm(request.POST)","        if comment_form.is_valid():","            user = request.user if request.user else 'anonymous'","            comment = Comment(user=user,","                                comment=comment_form.cleaned_data['comment'],","                                comment_date=timezone.now())","            comment.save()","            return redirect(ticket_detail, ticket.pk)","    else:","        comment_form = CommentForm()","    ","    return render(request, 'ticket-detail.html', {'ticket': ticket, 'comments': comments, 'comment_form': comment_form})","    ","","@login_required","def create_bug(request):","    if request.method == \"POST\":","        form = TicketForm(request.POST, request.FILES)","        if form.is_valid():","            ticket = Ticket(title=form.cleaned_data['title'],","                            summary=form.cleaned_data['summary'],","                            ticket_type='Bug',","                            screenshot=form.cleaned_data['screenshot'],","                            creator=request.user,","                            initiation_date=timezone.now())","            ticket.save()","            return redirect(ticket_detail, ticket.pk)","    else:","        form = TicketForm()","    return render(request, 'create-bug.html', {'form': form})","    ","    ","@login_required","def create_feature_request(request):","    if request.method==\"POST\":","        ticket_form = TicketForm(request.POST, request.FILES)","        payment_form = PaymentForm(request.POST)","        ","        if ticket_form.is_valid() and payment_form.is_valid():","            ticket = Ticket(title=ticket_form.cleaned_data['title'],","                                summary=ticket_form.cleaned_data['summary'],","                                ticket_type='Feature Request',","                                creator=request.user,","                                initiation_date=timezone.now())","            ticket.save()","            try:","                customer = stripe.Charge.create(amount = 3000,","                                                currency = \"eur\",","                                                description = request.user.email,","                                                card = payment_form.cleaned_data['stripe_id'],","                                                )","            except:","                messages.error(request, \"Your card was declined\")","                ","                if customer.paid:","                    messages.error(request, \"Your payment was successful\")","                    return redirect(ticket_detail, ticket.id)","                ","            else:","                     messages.error(request, \"Your payment was successful\")","                     return redirect(ticket_detail, ticket.id)   ","        else:","            print(payment_form.errors)","            messages.error(request, \"We were unable to take payment with that card\")","            ","    else:","        ticket_form = TicketForm()","        payment_form = PaymentForm()","        ","    return render(request, \"create-feature-request.html\", {'ticket_form': ticket_form, ","                                            'payment_form': payment_form,","                                            'publishable': settings.STRIPE_PUBLISHABLE})","                                            ","                                            ","@login_required","def edit_ticket(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk) if pk else None","    if request.method == \"POST\":","        form = TicketForm(request.POST, request.FILES, instance=ticket)","        if form.is_valid():","            ticket.title = form.cleaned_data['title']","            ticket.summary = form.cleaned_data['summary']","            ticket.save()","            return redirect(ticket_detail, ticket.pk)","    else:","        form = TicketForm(instance=ticket)","        html_page = 'edit-bug.html' if ticket.ticket_type == 'Bug' else 'edit-feature-request.html'","    return render(request, html_page, {'form': form})","    ","","@login_required","def delete_ticket(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    ticket.delete()","    return redirect(reverse('index'))","","","@login_required","def change_status_backlog(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    if ticket.completion_date:","        ticket.completion_date = None","    ticket.status = 'Backlog'","    ticket.save()","    return redirect(ticket_detail, ticket.id) ","  ","    ","@login_required","def change_status_in_progress(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    if ticket.completion_date:","        ticket.completion_date = None","    ticket.status = 'In Progress'","    ticket.save()","    return redirect(ticket_detail, ticket.id) ","    ","@login_required","def change_status_complete(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    ","    subject = \"Unicorn Attractor - Ticket #\" + str(ticket.id)","    from_email, to = 'lubaninondo@yahoo.com', request.user.email","    html_content = \"<p>Hi \" + ticket.creator + \"</p><p>You raised the below ticket on our website:</p><p><strong>TYPE:</strong> \" + ticket.ticket_type + \"</p><p><strong>TITLE:</strong> \" + ticket.title + \"</p><p>This email is to let you know this ticket has been completed. Thanks again for raising your issue.</p><p>Many thanks,</p><p>The Unicorn Attractor Team</p>\" ","    msg = EmailMessage(subject, html_content, from_email, [to])","    msg.content_subtype = \"html\"","    msg.send()","                ","    ticket.status = 'Complete'","    ticket.completion_date = timezone.now()","    ticket.save()","    return redirect(ticket_detail, ticket.id)"],"id":814},{"start":{"row":0,"column":0},"end":{"row":205,"column":45},"action":"insert","lines":["from django.shortcuts import render, reverse, redirect, get_object_or_404","from django.contrib.auth.decorators import login_required","from django.core.mail import EmailMessage","from django.contrib import messages","from django.utils import timezone","from django.conf import settings","from .models import Ticket","from .forms import TicketForm, PaymentForm","from comments.models import Comment","from comments.forms import CommentForm","import stripe","","stripe.api_key = SETTINGS.STRIPE_PUBLISHABLE","","# Create your views here.","def all_tickets(request, sort=None):","    if sort == 'bugs':","        tickets = Ticket.objects.filter(ticket_type='Bug')","    elif sort =='feature_requests':","        tickets = Ticket.objects.filter(ticket_type='Feature Request')","    else:","        tickets = Ticket.objects.all()","    return render(request, 'index.html', {'tickets': tickets})","    ","","@login_required    ","def upvote(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    ticket.upvotes += 1","    ticket.save()","    messages.error(request, \"Upvote recorded!\")","    return redirect(ticket_detail, ticket.pk)","    ","@login_required","def upvote_payment(request, pk):","    ","    ticket = get_object_or_404(Ticket, pk=pk)","    ","    if request.method==\"POST\":","        payment_form = PaymentForm(request.POST)","        if payment_form.is_valid():","            try:","                customer = stripe.Charge.create(amount = 500,","                                                currency = \"eur\",","                                                description = request.user.email,","                                                card = payment_form.cleaned_data['stripe_id'],","                                                )","            except:","                messages.error(request, \"Your card was declined\")","                ","            if customer.paid:","                messages.error(request, \"Your payment was successful\")","                new_total = float(ticket.total_paid) + (customer.amount/100)","                ticket.total_paid = new_total","                ticket.save()","                return redirect(upvote, ticket.id)","                ","            else:","                messages.error(request, \"Unable to take payment\")","        ","        else:","            print(payment_form.errors)","            messages.error(request, \"We were unable to take payment with that card\")","            ","    else:","        payment_form = PaymentForm()","        ","    return render(request, \"upvote-payment.html\", {'ticket': ticket, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})","                ","    ","def ticket_detail(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    comments = Comment.objects.filter(comment='user')","    ","    if request.method == \"POST\":","        comment_form = CommentForm(request.POST)","        if comment_form.is_valid():","            user = request.user if request.user else 'anonymous'","            comment = Comment(user=user,","                                comment=comment_form.cleaned_data['comment'],","                                comment_date=timezone.now())","            comment.save()","            return redirect(ticket_detail, ticket.pk)","    else:","        comment_form = CommentForm()","    ","    return render(request, 'ticket-detail.html', {'ticket': ticket, 'comments': comments, 'comment_form': comment_form})","    ","","@login_required","def create_bug(request):","    if request.method == \"POST\":","        form = TicketForm(request.POST, request.FILES)","        if form.is_valid():","            ticket = Ticket(title=form.cleaned_data['title'],","                            summary=form.cleaned_data['summary'],","                            ticket_type='Bug',","                            screenshot=form.cleaned_data['screenshot'],","                            creator=request.user,","                            initiation_date=timezone.now())","            ticket.save()","            return redirect(ticket_detail, ticket.pk)","    else:","        form = TicketForm()","    return render(request, 'create-bug.html', {'form': form})","    ","    ","@login_required","def create_feature_request(request):","    if request.method==\"POST\":","        ticket_form = TicketForm(request.POST, request.FILES)","        payment_form = PaymentForm(request.POST)","        ","        if ticket_form.is_valid() and payment_form.is_valid():","            ticket = Ticket(title=ticket_form.cleaned_data['title'],","                                summary=ticket_form.cleaned_data['summary'],","                                ticket_type='Feature Request',","                                creator=request.user,","                                initiation_date=timezone.now())","            ticket.save()","            try:","                customer = stripe.Charge.create(amount = 3000,","                                                currency = \"eur\",","                                                description = request.user.email,","                                                card = payment_form.cleaned_data['stripe_id'],","                                                )","            except:","                messages.error(request, \"Your card was declined\")","                ","                if customer.paid:","                    messages.error(request, \"Your payment was successful\")","                    return redirect(ticket_detail, ticket.id)","                ","            else:","                     messages.error(request, \"Your payment was successful\")","                     return redirect(ticket_detail, ticket.id)   ","        else:","            print(payment_form.errors)","            messages.error(request, \"We were unable to take payment with that card\")","            ","    else:","        ticket_form = TicketForm()","        payment_form = PaymentForm()","        ","    return render(request, \"create-feature-request.html\", {'ticket_form': ticket_form, ","                                            'payment_form': payment_form,","                                            'publishable': settings.STRIPE_PUBLISHABLE})","                                            ","                                            ","@login_required","def edit_ticket(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk) if pk else None","    if request.method == \"POST\":","        form = TicketForm(request.POST, request.FILES, instance=ticket)","        if form.is_valid():","            ticket.title = form.cleaned_data['title']","            ticket.summary = form.cleaned_data['summary']","            ticket.save()","            return redirect(ticket_detail, ticket.pk)","    else:","        form = TicketForm(instance=ticket)","        html_page = 'edit-bug.html' if ticket.ticket_type == 'Bug' else 'edit-feature-request.html'","    return render(request, html_page, {'form': form})","    ","","@login_required","def delete_ticket(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    ticket.delete()","    return redirect(reverse('index'))","","","@login_required","def change_status_backlog(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    if ticket.completion_date:","        ticket.completion_date = None","    ticket.status = 'Backlog'","    ticket.save()","    return redirect(ticket_detail, ticket.id) ","  ","    ","@login_required","def change_status_in_progress(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    if ticket.completion_date:","        ticket.completion_date = None","    ticket.status = 'In Progress'","    ticket.save()","    return redirect(ticket_detail, ticket.id) ","    ","@login_required","def change_status_complete(request, pk):","    ticket = get_object_or_404(Ticket, pk=pk)","    ","    subject = \"Unicorn Attractor - Ticket #\" + str(ticket.id)","    from_email, to = 'lubaninondo@yahoo.com', request.user.email","    html_content = \"<p>Hi \" + ticket.creator + \"</p><p>You raised the below ticket on our website:</p><p><strong>TYPE:</strong> \" + ticket.ticket_type + \"</p><p><strong>TITLE:</strong> \" + ticket.title + \"</p><p>This email is to let you know this ticket has been completed. Thanks again for raising your issue.</p><p>Many thanks,</p><p>The Unicorn Attractor Team</p>\" ","    msg = EmailMessage(subject, html_content, from_email, [to])","    msg.content_subtype = \"html\"","    msg.send()","                ","    ticket.status = 'Complete'","    ticket.completion_date = timezone.now()","    ticket.save()","    return redirect(ticket_detail, ticket.id)"]}],[{"start":{"row":12,"column":24},"end":{"row":12,"column":25},"action":"remove","lines":["S"],"id":815},{"start":{"row":12,"column":23},"end":{"row":12,"column":24},"action":"remove","lines":["G"]},{"start":{"row":12,"column":22},"end":{"row":12,"column":23},"action":"remove","lines":["N"]},{"start":{"row":12,"column":21},"end":{"row":12,"column":22},"action":"remove","lines":["I"]},{"start":{"row":12,"column":20},"end":{"row":12,"column":21},"action":"remove","lines":["T"]},{"start":{"row":12,"column":19},"end":{"row":12,"column":20},"action":"remove","lines":["T"]},{"start":{"row":12,"column":18},"end":{"row":12,"column":19},"action":"remove","lines":["E"]},{"start":{"row":12,"column":17},"end":{"row":12,"column":18},"action":"remove","lines":["S"]}],[{"start":{"row":12,"column":17},"end":{"row":12,"column":18},"action":"insert","lines":["s"],"id":816},{"start":{"row":12,"column":18},"end":{"row":12,"column":19},"action":"insert","lines":["e"]},{"start":{"row":12,"column":19},"end":{"row":12,"column":20},"action":"insert","lines":["t"]},{"start":{"row":12,"column":20},"end":{"row":12,"column":21},"action":"insert","lines":["t"]}],[{"start":{"row":12,"column":17},"end":{"row":12,"column":21},"action":"remove","lines":["sett"],"id":817},{"start":{"row":12,"column":17},"end":{"row":12,"column":25},"action":"insert","lines":["settings"]}],[{"start":{"row":12,"column":43},"end":{"row":12,"column":44},"action":"remove","lines":["E"],"id":818},{"start":{"row":12,"column":42},"end":{"row":12,"column":43},"action":"remove","lines":["L"]},{"start":{"row":12,"column":41},"end":{"row":12,"column":42},"action":"remove","lines":["B"]},{"start":{"row":12,"column":40},"end":{"row":12,"column":41},"action":"remove","lines":["A"]},{"start":{"row":12,"column":39},"end":{"row":12,"column":40},"action":"remove","lines":["H"]},{"start":{"row":12,"column":38},"end":{"row":12,"column":39},"action":"remove","lines":["S"]},{"start":{"row":12,"column":37},"end":{"row":12,"column":38},"action":"remove","lines":["I"]},{"start":{"row":12,"column":36},"end":{"row":12,"column":37},"action":"remove","lines":["L"]},{"start":{"row":12,"column":35},"end":{"row":12,"column":36},"action":"remove","lines":["B"]},{"start":{"row":12,"column":34},"end":{"row":12,"column":35},"action":"remove","lines":["U"]},{"start":{"row":12,"column":33},"end":{"row":12,"column":34},"action":"remove","lines":["P"]}],[{"start":{"row":12,"column":33},"end":{"row":12,"column":34},"action":"insert","lines":["S"],"id":819},{"start":{"row":12,"column":34},"end":{"row":12,"column":35},"action":"insert","lines":["E"]},{"start":{"row":12,"column":35},"end":{"row":12,"column":36},"action":"insert","lines":["C"]}],[{"start":{"row":12,"column":36},"end":{"row":12,"column":37},"action":"insert","lines":["R"],"id":820},{"start":{"row":12,"column":37},"end":{"row":12,"column":38},"action":"insert","lines":["E"]},{"start":{"row":12,"column":38},"end":{"row":12,"column":39},"action":"insert","lines":["T"]},{"start":{"row":12,"column":39},"end":{"row":12,"column":40},"action":"insert","lines":[";"]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":14,"column":25},"end":{"row":14,"column":25},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1570046394750,"hash":"fb1dd006476304315d67ff60c64e8181c8b3d24f"}