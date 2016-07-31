$(function () {
  $("a[href^='http']").attr('target','_blank');
  $("a[href^='//']").attr('target','_blank');
  $('a[rel="external"]').attr('target', '_blank');
  $("[rel='tooltip']").tooltip();
});
