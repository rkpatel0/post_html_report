
function MaxFire_HomePage_SlideshowB101(args)
{if(!args.eid){return(false);}
var elem=dyna.elem(args.eid);if(!elem){return(false);}
elem.max_obj=this;++dyna.icount;if(!args.slide_order&&args.slide_count>0){args.slide_order=[];for(var i=1;i<=args.slide_count;++i){args.slide_order.push(i);}}
if(!args.slide_order){return(false);}
var first_snum=args.slide_order[0];if(!first_snum){return(false);}
this.num_slides=args.slide_order.length;this.curr_snum=1;for(key in args){this[key]=args[key];}
if(!this.vname){this.vname=this.name;}
this.screen_eid=this.name+"-screen";this.screen_elem=dyna.elem(this.screen_eid);this.tray_eid=this.name+"-tray";this.tray_elem=dyna.elem(this.tray_eid);this.tween1=new Fx.Tween(this.tray_eid,{unit:'px',duration:'long',transition:'sine:in:out',link:'ignore',property:'left'});this.tween1.addEvent('complete',this.methcall(this,this.tween1_complete));this.auto={active:false,state:'play',command:'',timer:0,intro_period:8000,view_period:7000,max_loops:1,num_loops:0,inc_loops:1};this.afk={active:true,state:'run',timer:0,wait_period:3*60000};this.init_slide_map();this.init_screen();this.auto_init();return(this);}
MaxFire_HomePage_SlideshowB101.prototype.init_slide_map=function()
{var min_pos=0;var max_pos=this.num_slides-1;this.slide_map={};for(var i=0;i<this.num_slides;++i){var snum=this.slide_order[i];var sname="s"+snum;var rec={"snum":snum,"sname":sname,"pos":i};rec.next_pos=i==max_pos?0:i+1;rec.prev_pos=i==min_pos?max_pos:i-1;rec.next_snum=rec.next_pos+1;rec.prev_snum=rec.prev_pos+1;rec.elem=dyna.elem(this.name+"-"+sname);this.slide_map[sname]=rec;}
return(this.slide_map);}
MaxFire_HomePage_SlideshowB101.prototype.prep_slides=function()
{}
MaxFire_HomePage_SlideshowB101.prototype.auto_init=function()
{var big_num=1000000000;if(this.auto.max_loops<0||this.auto.max_loops=='nolimit'){this.auto.max_loops=big_num;}
this.auto.begin_func=this.vname+".auto_begin";this.auto.view_func=this.vname+".auto_view";this.auto.select_func=this.vname+".auto_select";}
MaxFire_HomePage_SlideshowB101.prototype.auto_interrupt=function()
{this.auto_reset();this.auto_timer_clear();this.auto_inc_loops();this.auto_snooze();}
MaxFire_HomePage_SlideshowB101.prototype.auto_intro=function()
{if(!this.auto.active){return(0);}
if(this.num_slides<=1){return(0);}
var cb_func=this.auto.begin_func+"()";this.afk.timer=setTimeout(cb_func,this.auto.intro_period);}
MaxFire_HomePage_SlideshowB101.prototype.auto_snooze=function()
{if(!this.auto.active){return(0);}
if(this.num_slides<=1){return(0);}
var cb_func=this.auto.begin_func+"()";this.afk.timer=setTimeout(cb_func,this.afk.wait_period);}
MaxFire_HomePage_SlideshowB101.prototype.auto_begin=function()
{this.auto_timer_clear();var first_snum=this.first_snum();var view_period=this.auto.view_period;if(this.curr_snum==first_snum){view_period=1000;}
else{this.auto_select(first_snum);}
var cb_func=this.auto.view_func+"()";this.auto.timer=setTimeout(cb_func,view_period);}
MaxFire_HomePage_SlideshowB101.prototype.auto_reset=function()
{this.auto.state="play";this.auto.num_loops=0;}
MaxFire_HomePage_SlideshowB101.prototype.auto_timer_clear=function()
{if(this.auto.timer){clearTimeout(this.auto.timer);}
this.auto.timer=0;if(this.afk.timer){clearTimeout(this.afk.timer);}
this.afk.timer=0;}
MaxFire_HomePage_SlideshowB101.prototype.auto_inc_loops=function()
{if(this.auto.inc_loops){this.auto.max_loops+=this.auto.inc_loops;this.auto.inc_loops=0;}}
MaxFire_HomePage_SlideshowB101.prototype.auto_view=function()
{var command=this.auto_next();var view_period=this.auto.view_period;var first_snum=this.first_snum();var next_snum=this.next_snum();var view_func=this.auto.view_func+"()";if(command=="done"){this.auto_inc_loops();this.auto_select(first_snum);this.auto_interrupt();}
else if(command=="next"){this.auto_select(next_snum);this.auto.timer=setTimeout(view_func,view_period);}
else if(command=="first"){this.auto_select(first_snum);this.auto.timer=setTimeout(view_func,view_period);}
else if(command=="pause"){}
else{;}}
MaxFire_HomePage_SlideshowB101.prototype.auto_next=function()
{this.auto_timer_clear();this.auto.command="done";if(this.auto.state=="pause"){this.auto.command="pause";return(this.auto.command);}
if(this.num_slides<=1){return(this.auto.command);}
if(!this.auto.active){return(this.auto.command);}
var first_snum=this.first_snum();var curr_srec=this.slide_map["s"+this.curr_snum];var next_srec=this.slide_map["s"+curr_srec.next_snum];var loop_ending=next_srec.pos==0;var cycle_ending=false;if(loop_ending){++this.auto.num_loops;cycle_ending=this.auto.num_loops>=this.auto.max_loops;if(cycle_ending){this.auto.num_loops=0;}}
if(cycle_ending){return(this.auto.command);}
this.auto.command="next";return(this.auto.command);}
MaxFire_HomePage_SlideshowB101.prototype.auto_select=function(snum)
{this.select_slide(snum);}
MaxFire_HomePage_SlideshowB101.prototype.toggle_display=function()
{dyna.toggle_elem(this.screen_eid);dyna.toggle_elem(this.tray_eid);}
MaxFire_HomePage_SlideshowB101.prototype.toggle_screen=function()
{dyna.toggle_elem(this.screen_eid);}
MaxFire_HomePage_SlideshowB101.prototype.init_screen=function()
{return(this.set_screen(this.curr_snum));}
MaxFire_HomePage_SlideshowB101.prototype.set_screen=function(snum)
{var sname="s"+snum;var screen_elem=this.screen_elem;var slide_elem=this.slide_map[sname].elem;if(!screen_elem||!slide_elem){return(false);}
var value=dyna.get_style(slide_elem,'background-image');screen_elem.style.backgroundImage=value;screen_elem.innerHTML=slide_elem.innerHTML.replace(/-s\d+-text/,"-s0-text");}
MaxFire_HomePage_SlideshowB101.prototype.select_slide=function(snum)
{var sname='s'+snum;var srec=this.slide_map[sname];if(typeof(srec)=="undefined"){return(false);}
if(this.tween1.isRunning()){return(false);}
if(snum==this.curr_snum){return(false);}
var curr_pos=this.compute_tray_position(this.curr_snum);var new_pos=this.compute_tray_position(snum);this.resize_tray();this.toggle_display();this.anim_snum=snum;this.control_update_begin(snum);this.animate_tray(curr_pos,new_pos);return(true);}
MaxFire_HomePage_SlideshowB101.prototype.click_slide=function(snum)
{if(!snum||snum==''){snum=this.curr_snum;}
var elem=dyna.elem("hss-s"+snum+"-link");if(!elem){alert("Bad slide mojo.1: "+snum);return(false);}
this.auto_timer_clear();window.location=elem.href;}
MaxFire_HomePage_SlideshowB101.prototype.toggle_tray=function()
{dyna.toggle_elem(this.tray_eid);}
MaxFire_HomePage_SlideshowB101.prototype.animate_tray=function(start,finish)
{this.text_eid="hss-s"+this.curr_snum+"-text";this.text_elem=dyna.elem(this.text_eid);this.tween2=new Fx.Tween(this.text_eid,{unit:'px',duration:'600',transition:'sine:in:out',link:'ignore',property:'left'});this.tween2.addEvent('complete',this.methcall(this,this.tween2_complete));this.set_screen(this.anim_snum);this.tween1.start(start,finish);this.tween2.start(0,-2000);}
MaxFire_HomePage_SlideshowB101.prototype.tween1_complete=function()
{var next_snum=this.anim_snum;this.toggle_display();this.control_update_end(next_snum);this.prev_snum=this.curr_snum;this.curr_snum=next_snum;this.text_elem.style.left="0px";this.text_elem.style.display="";}
MaxFire_HomePage_SlideshowB101.prototype.tween2_complete=function()
{this.text_elem.style.display="none";}
MaxFire_HomePage_SlideshowB101.prototype.position_tray=function(snum)
{var pos=this.compute_tray_position(snum);var tray_elem=dyna.elem(this.name+"-tray");tray_elem.style.left=pos+"px";}
MaxFire_HomePage_SlideshowB101.prototype.compute_tray_position=function(snum)
{var page_width=this.get_active_page_width();return(-page_width*(snum-1));}
MaxFire_HomePage_SlideshowB101.prototype.resize_tray=function()
{var page_width=this.get_active_page_width();for(var i=0;i<this.num_slides;++i){var sname="s"+this.slide_order[i];this.slide_map[sname].elem.style.width=page_width+"px";}}
MaxFire_HomePage_SlideshowB101.prototype.control_select_slide=function(snum)
{if(this.auto.active){this.auto_interrupt();}
return(this.select_slide(snum));}
MaxFire_HomePage_SlideshowB101.prototype.control_update_begin=function(next_snum)
{}
MaxFire_HomePage_SlideshowB101.prototype.control_update_end=function(next_snum)
{}
MaxFire_HomePage_SlideshowB101.prototype.first_snum=function()
{return(this.slide_order[0]);}
MaxFire_HomePage_SlideshowB101.prototype.prev_snum=function()
{return(this.slide_map["s"+this.curr_snum].prev_snum);}
MaxFire_HomePage_SlideshowB101.prototype.next_snum=function()
{return(this.slide_map["s"+this.curr_snum].next_snum);}
MaxFire_HomePage_SlideshowB101.prototype.get_active_page_width=function()
{var elem=dyna.elem(this.name);return(elem.clientWidth);}
MaxFire_HomePage_SlideshowB101.prototype.methcall=function(obj,method)
{return(function(){return(method.apply(obj,arguments));});}