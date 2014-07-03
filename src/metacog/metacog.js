//set main namespace
goog.provide('metacog');

//get requirements
goog.require('metacog.CircleScene');
goog.require('metacog.SliderScene');
goog.require('metacog.BetScene');
goog.require('metacog.TrialLog');

goog.require('lime.Director');
goog.require('lime.Scene');
goog.require('lime.Layer');
goog.require('lime.Circle');
goog.require('lime.Label');
goog.require('lime.animation.Spawn');
goog.require('lime.animation.FadeTo');
goog.require('lime.animation.ScaleTo');
goog.require('lime.animation.MoveTo');

var config = {
  screen_width: 1024,
  screen_height: 768,
  diametro_max: 768 / 4,
  circle_size: [151,150,152,
                154,155,156,
                157,158,159],
  circle_color: [0,0,0,0,0,0,0,0,0],
  /*circle_color: [20,40,60,80,100,120,140,160,180],*/
  size_pattern: [96, 92, 97, 99, 98, 97, 93, 95],
  MAX_SIZE: 160,
  initial_treshold: 0.5,
  difficulty_step: 1.8,
  trial_amount: 30
};

metacog.saveLog = function() {
  var data = JSON.stringify({sujeto: "chudi", log: metacog.trials.trial_results});
  $.ajax("/createlog", {
      data: data,
      contentType : "application/json",
      type : "POST"
  }); 
}

metacog.start = function(){


  lime.Label.defaultFont = "Arial, Helvetica, sans-serif";

  metacog.director = new lime.Director(document.body,config.screen_width,config.screen_height);
  metacog.trials = new metacog.TrialLog(config.initial_treshold);
  metacog.create_trial();

};

metacog.create_trial = function() {
  if(metacog.trials.trial_results.length > config.trial_amount){
    metacog.saveLog();
    return;
  }
  metacog.trials.new_trial();

  var circle_scene = metacog.CircleScene.createScene(metacog.trials.get_scale());

  metacog.trials.current_trial.time_choosing_circle = goog.now();

  metacog.director.replaceScene(circle_scene);
};

metacog.end_trial = function() {
  console.log(metacog.trials.trial_results[metacog.trials.trial_results.length - 1]);
  console.log(metacog.trials.score);
};

metacog.new_trial = function () {
  metacog.end_trial();
  metacog.create_trial();
};

metacog.finish_selection = function() {
  metacog.trials.current_trial.time_choosing_circle =  goog.now() - metacog.trials.current_trial.time_choosing_circle;
  metacog.bet_or_trust();    
};

metacog.bet_or_trust = function() {
  if(Math.random() > 0.5) {
    metacog.bet();
  } else {
    metacog.slider();
  }
};

metacog.manage_bet_sure = function() {
  metacog.trials.current_trial.time_betting =  goog.now() - metacog.trials.current_trial.time_betting;
  metacog.new_trial();
};

metacog.manage_bet_not_sure = function() {
  metacog.trials.current_trial.time_betting =  goog.now() - metacog.trials.current_trial.time_betting;
  metacog.new_trial();
};

metacog.bet = function() {
  var bet_scene = metacog.BetScene.createScene();
  metacog.trials.current_trial.time_betting =  goog.now();
  metacog.trials.current_trial.second_screen = "bet";
  metacog.director.replaceScene(bet_scene);
};

metacog.slider = function() {
  metacog.trials.current_trial.second_screen = "trust";
  metacog.trials.current_trial.time_trust =  goog.now();
  var slider_scene = metacog.SliderScene.createScene();
  metacog.director.replaceScene(slider_scene);
};

metacog.manage_slider_fin = function() {
  metacog.trials.current_trial.time_trust =  goog.now() - metacog.trials.current_trial.time_trust;
  metacog.new_trial();
}

//this is required for outside access after code is compiled in ADVANCED_COMPILATIONS mode
goog.exportSymbol('metacog.start', metacog.start);