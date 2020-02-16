function showPhone() {
  var a = 40531;
  var b = 37042;
  var c = a * a + b * b + 1;
  console.log(c);
  console.log(c.toString());
  console.log(formatPhoneNumber(c.toString()));
  $("#reveal_phone").html(formatPhoneNumber(c.toString()));
}

function sendMessage() {
  var name = $('#send_name').val();
  if (name === null) {
    name = "A friend";
  }
  var subject = "[Greetings] " + name + " has a message for you";
  var body =
      $("#send_message").val() + "\n" + name + "\n" + $("#sender_email").val();
  var suffix = "abc.com";
  window.open('mailto:me' + String.fromCharCode(64) + suffix + '?subject=' +
              subject + '&body=' + body);
}

function bibtexOnClick() {
  $('#apa-text').hide();
  $('#mla-text').hide();
  $('#bibtex-text').show();
}

function apaOnClick() {
  $('#bibtex-text').hide();
  $('#mla-text').hide();
  $('#apa-text').show();
}

function mlaOnClick() {
  $('#bibtex-text').hide();
  $('#apa-text').hide();
  $('#mla-text').show();
}


function init() {
  // Opens in new window for external webpage.
  $('a[href^="http://"], a[href^="https://"], a[href$=".pdf"]', )
      .attr('target', '_blank');
  $(".seo").hide();

  // Shows email and phone.
  $("#reveal_email").on({'touchstart': function() { showEmail(); }});
  $("#reveal_email").click(function() { showEmail(); });
  $("#reveal_phone").on({'touchstart': function() { showPhone(); }});
  $("#reveal_phone").click(function() { showPhone(); });

  // Sends email events.
  $("#send_email").click(function() { sendMessage(); });
  $("#send_email").on({'touchstart': function() { sendMessage(); }});

  // Citation
  $('.cite').popup();
}

$(document).ready(function() { init(); });
