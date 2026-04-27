// ---------------------------------------------------------------------------
// Jumpscare
//    using the Template design pattern.
// ---------------------------------------------------------------------------

// base class for the others to base themselves off of
class Jumpscares{
    constructor(gif,audio){
        this.gif = gif;
        this.audio = audio;
    }
execute(reaction){
    let scare = new Audio(this.audio);
    scare.play();

    reaction.src = "";
    reaction.src = this.gif;
    reaction.style.display = "block";

    setTimeout(() => {
      reaction.style.display = "none";
      scare.pause();
      scare.currentTime = 0;
    }, 800);
  }
}

class Foxy extends Jumpscares{
    constructor(){
        super(
            "/static/images/foxy-jumpscare.gif",
            "/static/audio/five-nights-at-freddys-2-full-scream-sound.mp3"
        );
    }
}
class Puppet extends Jumpscares{
    constructor(){
        super(
            "/static/images/puppet-jumpscare.gif",
            "/static/audio/five-nights-at-freddys-2-full-scream-sound.mp3"
        );
    }
}
class Trap extends Jumpscares{
    constructor(){
        super(
            "/static/images/springtrap_animation.gif",
            "/static/audio/fnaf-3-scream-sound.mp3"
        );
    }
}
// this calls a different jumpscare for each button pressed 
class JumpscareTotallity {
  constructor(reaction, chance = 1/2) {
    this.reaction = reaction;
    this.chance = chance;
    this.buttonStrategies = {
      "faculty-button": new Foxy(),
      "schedule-button": new Puppet(),
      "labs-button":    new Trap(),
    };
  }
// this function decides the actual percentage chance of getting jumpscared 
  handleClick(targetId) {
    const strategy = this.buttonStrategies[targetId];

    if (strategy) {
      if (Math.random() < this.chance) {
        strategy.execute(this.reaction);
      }
    } else {
      this.reaction.style.display = "none";
      this.reaction.src = "";
    }
  }
}
// Actual jumpscare positioning and logic so
export function spawn_jumpscare() {
  const reaction = document.getElementById("fnaf-image");
  const toggle = document.querySelector("#secret-toggle input[type='checkbox']");
  const context = new JumpscareContext(reaction);

  document.addEventListener("click", (e) => {
    if (!toggle.checked) return;
    context.handleClick(e.target.id);
  });
}

// Self-initializing so no import needed in other files
spawn_jumpscare();