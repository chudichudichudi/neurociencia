goog.provide('metacog.SliderScene');

goog.require('lime.Scene');
goog.require('lime.Layer');
goog.require('lime.Circle');
goog.require('lime.Label');
goog.require('lime.animation.FadeTo');
goog.require('lime.animation.MoveTo');
goog.require('lime.animation.MoveBy');
goog.require('lime.animation.ScaleBy');
goog.require('lime.animation.Spawn');

metacog.SliderScene = function(){
	//goog.base(this);
};

metacog.SliderScene.create_title_layer= function (argument) {
	var layer_title = new lime.Layer().setPosition(0,0);
	var title = new lime.Label().setPosition(512 ,50).setFontFamily("Arial, Helvetica, sans-serif").setText("Are you sure?").setFontSize(50).setFontWeight("bold").setFill(200,100,100,.1).setSize(800,70);;
	
	layer_title.appendChild(title);

	return layer_title;
};

metacog.SliderScene.create_slider_layer = function() {
	var posy = 50;
	var sliderWidth = config.screen_width - 250;
	var defaultValue= sliderWidth / 2;
	var width_pos = 125;
  var height_pos = config.screen_height / 2;
  var slider_sprite = new lime.Sprite().setSize(150, 300).setFill(0, 100, 100, 1).setPosition(defaultValue, posy);
  var layer = new lime.Layer().setPosition(width_pos,height_pos);

  goog.events.listen(slider_sprite, ['mousedown', 'touchstart'],function(e) {
  	var drag = new lime.events.Drag(e,false,new goog.math.Box(posy, sliderWidth, posy, 0));

		goog.events.listen(drag, lime.events.Drag.Event.MOVE,function(){
			var value = this.getPosition().x;
			metacog.trials.current_trial.trust = Math.floor((value/sliderWidth).toFixed(2) * 100);
		},false,slider_sprite);

	});

	var background_slider = new lime.Sprite().setSize(sliderWidth, 100).setFill(100, 0, 100, 1).setPosition(defaultValue, posy);

	/* Esto lo dejaria para hacer que cuando clickees la parte de atras del slider funcione todo oka
	goog.events.listen(background_slider, ['mousedown', 'touchstart'],function(e) {
		//var move_anim = new lime.animation.MoveBy(e.position.x, 0).setDuration(1.5);
		var move_anim = new lime.animation.MoveBy(e.position.x, 0).setDuration(0.5);
		slider_sprite.runAction(move_anim);
		console.log(e.position.x + ' ' + e.position.y);

 		e.swallow(['mousedown','touchstart'],function(){
        this.setFill('#0c0'); // ball is colored back to green when interaction ends
    },false, this);

	}, false, this);
	*/
	layer.appendChild(background_slider);
  layer.appendChild(slider_sprite);

	return layer;
};

metacog.SliderScene.create_done_button = function () {
	var layer_button = new lime.Layer().setPosition(0,(config.screen_height / 4) * 3 );
	var done_button = new lime.Label().setPosition(config.screen_width / 2 ,75).setFontFamily("Arial, Helvetica, sans-serif").setText("Done").setFontSize(50).setFontWeight("bold");
	layer_button.appendChild(done_button);

	goog.events.listen(layer_button,['mousedown','touchstart'],function() {
		metacog.manage_slider_fin();
	});
	return layer_button;
};

metacog.SliderScene.createScene = function () {
	var layer_title = metacog.SliderScene.create_title_layer();
	var layer_slider = metacog.SliderScene.create_slider_layer();
	var layer_button = metacog.SliderScene.create_done_button();
	
	var scene = new lime.Scene();
	scene.appendChild(layer_slider);
	scene.appendChild(layer_title);
	scene.appendChild(layer_button);

  return scene;
};