<%inherit file="/base.mako"/>

<%!
import itertools
from decimal import Decimal
%>

<%
form_cycle = itertools.cycle(['even', 'odd'])
%>

## ToscaWidgets doesn't support dynamically generating the form fields
## themselves, so I'm mimicing its style but generating the form by
## hand

<p>Change how an expenditure is split up. Enter a percentage, or
something like a percentage, for each user. They don't have to add to
100.</p>

<p>You're editing an expenditure of ${c.expenditure.amount} by
${c.expenditure.spender.name} on ${c.expenditure.date}, described as
"${c.expenditure.description}"</p>

${h.form('', method='post')}
<form>
  <table>
    % for user in c.users:
      <%
        name = user.username
        try:
            percent = c.values[name]
        except TypeError:
            try:
                share = [s.share for s in c.expenditure.splits if s.user == user][0]
                percent = (Decimal(100) * Decimal(int(share)) / Decimal(int(c.expenditure.amount))).quantize(Decimal("0.001"))
            except IndexError:
                percent = Decimal(0)
      %>\
      <tr class="${form_cycle.next()}" id="${name}.container">
        <td class="labelcol">
          <label id="${name}.label" for="${name}" class="fieldlabel">${user.name}</label>
        </td>
        <td class="fieldcol">
          ${h.text(name, value=percent, class_="textfield required", id=name)}
          % if name in c.errors:
            <span class="fielderror">${c.errors[name]}</span>
          % endif
        </td>
      </tr>
    % endfor
    <tr class="${form_cycle.next()}" id="submit.container">
      <td class="labelcol"></td>
      <td class="fieldcol">
        ${h.submit(None, 'Submit', class_="submitbutton")}
      </td>
    </tr>
  </ul>
</form>
