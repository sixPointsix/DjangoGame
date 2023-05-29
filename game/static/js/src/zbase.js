export class AcGame{
    constructor(id, AcWingOs){
        this.id = id;
        this.$ac_game = $('#' + id);
        this.AcWingOS = AcWingOs;

        this.settings = new Settings(this);
        this.menu = new AcGameMenu(this);
        this.playground = new AcGamePlayground(this);

        this.start();
    }

    start() {
    }
}
