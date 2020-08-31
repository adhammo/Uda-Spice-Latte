import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Drink {
    id: number;
    title: string;
    recipe: Array<{
        name: string;
        color: string;
        parts: number;
    }>;
}

function drinkToJSON(drink: Drink) : string {
    return JSON.stringify({
        'title': drink.title,
        'recipe': drink.recipe
    });
}

@Injectable({
    providedIn: 'root',
})
export class DrinksService {
    url = environment.apiServerUrl;

    public items: { [key: number]: Drink } = {};

    constructor(private auth: AuthService, private http: HttpClient) {}

    getHeaders() {
        const header = {
            headers: new HttpHeaders().set('Authorization', `Bearer ${this.auth.activeJWT()}`).set('Content-Type', 'application/json'),
        };
        return header;
    }

    getDrinks() {
        if (this.auth.can('get:drinks-detail')) {
            this.http.get(this.url + '/drinks-detail', this.getHeaders()).subscribe((res: any) => {
                this.drinksToItems(res.drinks);
                console.log(res);
            });
        } else {
            this.http.get(this.url + '/drinks', this.getHeaders()).subscribe((res: any) => {
                this.drinksToItems(res.drinks);
                console.log(res);
            });
        }
    }

    saveDrink(drink: Drink) {
        if (drink.id >= 0) {
            this.http.patch(this.url + '/drinks/' + drink.id, drinkToJSON(drink), this.getHeaders()).subscribe((res: any) => {
                if (res.success) {
                    this.drinksToItems(res.drinks);
                }
            });
        } else {
            this.http.post(this.url + '/drinks', drinkToJSON(drink), this.getHeaders()).subscribe((res: any) => {
                if (res.success) {
                    this.drinksToItems(res.drinks);
                }
            });
        }
    }

    deleteDrink(drink: Drink) {
        this.http.delete(this.url + '/drinks/' + drink.id, this.getHeaders()).subscribe((res: any) => {
            if (res.success) {
                delete this.items[drink.id];
            }
        });
    }

    drinksToItems(drinks: Array<Drink>) {
        for (const drink of drinks) {
            this.items[drink.id] = drink;
        }
    }


}
