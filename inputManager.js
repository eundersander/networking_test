class InputManager {
  constructor() {
    this.keyHeld = {};
    this.keyDown = {};
    this.keyUp = {};

    // Binding the methods to the instance to make sure `this` refers to the instance 
    // inside the event listeners.
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleKeyUp = this.handleKeyUp.bind(this);

    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("keyup", this.handleKeyUp);
  }

  handleKeyDown(event) {
    // Only log first keyDown. This filters extra keyDown events coming from keyboard repeat.
    if (!this.keyHeld[event.key]) { 
      this.keyHeld[event.key] = true;
      this.keyDown[event.key] = true;
    }
  }

  handleKeyUp(event) {
    if (this.keyHeld[event.key]) { 
      this.keyHeld[event.key] = false;
      this.keyUp[event.key] = true;
    }
  }

  getSerializeState() {
    const obj = {
      keyHeld: this.keyHeld,
      keyDown: this.keyDown,
      keyUp: this.keyUp
    };
    return obj;
  }

  // returns true is the key is currently down
  getKey(key) {
    return !!this.keyHeld[key];  // returns true if key is pressed, otherwise false
  }

  // returns true if key was pressed on this frame
  getKeyDown(key) {
    return !!this.keyDown[key];
  }

  // returns true if key was released on this frame
  getKeyUp(key) {
    return !!this.keyUp[key];
  }

  onEndFrame() {
    this.keyUp = {}
    this.keyDown = {}
  }

  dispose() {
    // Remove event listeners to clean up when no longer needed
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("keyup", this.handleKeyUp);
  }
}