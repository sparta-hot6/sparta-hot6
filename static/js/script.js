window.onload = function () {
  function onClick() {
    document.querySelector(".modal_wrap").style.display = "block";
    document.querySelector(".black_bg").style.display = "block";
  }
  function offClick() {
    document.querySelector(".modal_wrap").style.display = "none";
    document.querySelector(".black_bg").style.display = "none";
  }

  document.getElementById("modal_btn").addEventListener("click", onClick);
  document.querySelector(".modal_close").addEventListener("click", offClick);

  $.ajax({
    type: "GET",
    url: "/api/profile",
    data: {},
    success: function (data) {
      const { name, login_id, profile_image, background_image } = data;
      $("#profile_name").text(name);
      bg_path = "/api/file/" + background_image;
      pf_path = "/api/file/" + profile_image;
      $("#back_img").attr("src", bg_path);
      $("#profile_img").attr("src", pf_path);
    },
  });
};
