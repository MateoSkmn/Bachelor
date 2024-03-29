import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { LimeComponent } from './features/lime/lime.component';
import { ModelComponent } from './features/model/model.component';
import { PageNotFoundComponent } from './features/page-not-found/page-not-found.component';

export const routes: Routes = [
    { path: '', redirectTo: 'data', pathMatch: 'full' },
    { path: 'data', component: HomeComponent },
    { path: 'model', component: ModelComponent },
    { path: 'lime', component: LimeComponent },
    { path: '**', component: PageNotFoundComponent }
];
