window.onload = function () {
  $.ajax({
    type: "GET",
    url: "/api/profile",
    data: {},
    success: function (data) {
      const { name, login_id, profile_image, background_image } = data;
      $("#profile_name").text(name);
      if (background_image) {
        bg_path = "/api/file/" + background_image;
        $("#back_img").attr("src", bg_path);
      }
      if (profile_image) {
        pf_path = "/api/file/" + profile_image;
        $("#profile_img").attr("src", pf_path);
      }
    },
  });
};
