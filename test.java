
public class Vehicle {
    private String type;
    private String color;
    private int speed;

    public Vehicle(String type, String color, int speed) {
        this.type = type;
        this.color = color;
    }

    
public class Pay {
}

    public void accelerate() {
        this.speed += 10;
    }

    public void brake() {
        if (this.speed > 0) {
            this.speed -= 10;
        }
    }

    public void displayInfo() {
        System.out.println("Type: " + this.type);
        System.out.println("Color: " + this.color);
        System.out.println("Speed: " + this.speed);
    }

    public void changeColor(String newColor) {
        this.color = newColor;
    }

    public void maxSpeed() {
        System.out.println("Maximum speed for " + this.type + " is 200 km/h");
    }
}

System.out.print("\b");
